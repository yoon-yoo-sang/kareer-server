import asyncio
from typing import List
from datetime import datetime

from celery import shared_task
from django.db import transaction
from django.utils import timezone

from insights.crawlers.google_crawler import GoogleCrawler
from insights.models import Insight, SearchKeyword
from insights.processors.gpt_processor import GptProcessor


def _categorize_insight(content: str) -> str:
    """
    컨텐츠를 분석하여 카테고리를 결정합니다.
    :param content: GPT가 추출한 컨텐츠
    :return: 카테고리
    """
    gpt_processor = GptProcessor(
        system_prompt="""
        주어진 텍스트를 분석하여 다음 카테고리 중 하나로 분류해주세요:
        - visa: 비자, 체류, 입국 관련 정보
        - culture: 한국 문화, 생활, 관습 관련 정보
        - industry: 산업, 기업, 경제 관련 정보
        
        응답은 카테고리 코드만 작성해주세요. (visa/culture/industry)
        """
    )
    
    category = gpt_processor.process(content).strip().lower()
    if category not in [choice[0] for choice in Insight.CategoryEnum.choices]:
        return Insight.CategoryEnum.INDUSTRY  # 기본값
    return category


@shared_task
def get_infos(search_word: str, num: int = 5) -> List[dict]:
    """
    Google Custom Search API를 사용하여 검색 결과를 가져오고,
    해당 링크를 크롤링하여 정보를 추출합니다.
    :param search_word: 검색어
    :param num: 검색 결과 개수
    :return: 저장된 인사이트 목록
    """
    google_crawler = GoogleCrawler()
    gpt_processor = GptProcessor(
        system_prompt=f"""
        HTML 내용을 읽고 검색어({search_word})와 관련된 내용을 추출해서 요약해주세요.
        불필요한 내용은 제외하고, 핵심적인 정보만 추출해주세요.
        한국에서 일하고 싶어하는 외국인에게 도움이 될만한 정보를 중심으로 추출해주세요.
        """
    )

    crawl_templates = asyncio.run(google_crawler.google_crawl_async(search_word, num=num))
    insights = []

    with transaction.atomic():
        for template in crawl_templates:
            try:
                content = gpt_processor.process(template.html)
                category = _categorize_insight(content)
                
                insight = Insight.objects.create(
                    search_word=search_word,
                    category=category,
                    content=content,
                    source_url=template.link
                )
                
                insights.append({
                    "id": insight.id,
                    "search_word": insight.search_word,
                    "category": insight.category,
                    "content": insight.content,
                    "source_url": insight.source_url
                })
                
            except Exception as e:
                print(f"Error processing template {template}: {e}")
                continue

    return insights


@shared_task
def daily_insight_collection():
    """
    매일 실행되어 활성화된 모든 검색어에 대해 인사이트를 수집합니다.
    """
    keywords = SearchKeyword.objects.filter(is_active=True)
    results = []
    
    for keyword in keywords:
        try:
            insights = get_infos(keyword.keyword)
            keyword.last_searched_at = timezone.now()
            keyword.save()
            
            results.append({
                "keyword": keyword.keyword,
                "insights_count": len(insights),
                "status": "success"
            })
        except Exception as e:
            results.append({
                "keyword": keyword.keyword,
                "error": str(e),
                "status": "error"
            })
    
    return results
