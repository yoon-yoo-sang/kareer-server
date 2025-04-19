import asyncio
from datetime import timedelta
from typing import List

from celery import shared_task
from django.db import transaction
from django.utils import timezone

from insights.crawlers.google_crawler import GoogleCrawler
from insights.models import (CultureInfo, IndustryInfo, Insight, SearchKeyword,
                             VisaInfo)
from insights.processors.html_llm_processor import GptProcessor
from insights.processors.insight_llm_processor import InfoProcessor


def _categorize_insight(content: str) -> str:
    """
    컨텐츠를 분석하여 카테고리를 결정합니다.
    :param content: GPT가 추출한 컨텐츠
    :return: 카테고리
    """
    gpt_processor = GptProcessor(
        model="gpt-3.5-turbo",
        system_prompt="""
        Classify the given text into one of the following categories:
        - visa: Information related to visas, residence, and entry
        - culture: Information related to Korean culture, lifestyle, and customs
        - industry: Information related to industries, companies, and economy
        
        Please respond with only the category code. (visa/culture/industry)
        """,
    )

    category = gpt_processor.process(content).strip().lower()
    if category not in [choice[0] for choice in Insight.CategoryEnum.choices]:
        return Insight.CategoryEnum.INDUSTRY  # 기본값
    return category


@shared_task
@transaction.atomic
def get_infos(search_word: str, num: int = 5) -> List[dict]:
    """
    Google Custom Search API를 사용하여 검색 결과를 가져오고,
    해당 링크를 크롤링하여 정보를 추출합니다.
    :param search_word: 검색어
    :param num: 검색 결과 개수
    :return: 저장된 인사이트 목록
    """
    google_crawler = GoogleCrawler()
    gpt_3_5_processor = GptProcessor(
        model="gpt-3.5-turbo",
        system_prompt=f"""
        Read the HTML content and extract information related to the search term ({search_word}).
        """,
    )
    gpt_4_processor = GptProcessor(
        model="gpt-4",
        system_prompt=f"""
        Exclude unnecessary information and extract only the key points.
        Focus on extracting information that would be helpful for foreigners who want to work in Korea.
        """,
    )

    crawl_templates = asyncio.run(
        google_crawler.google_crawl_async(search_word, num=num)
    )
    insights = []

    with transaction.atomic():
        for template in crawl_templates:
            try:
                if not template.html:
                    continue

                already_exist_insight = Insight.objects.filter(source_url=template.link)
                already_exist_insight_exists = already_exist_insight.exists()

                if (
                    already_exist_insight.exists()
                    and already_exist_insight.first().updated_at
                    > timezone.now() - timedelta(days=30)
                ):
                    continue

                content = gpt_3_5_processor.process(template.html)
                content = gpt_4_processor.process(content)

                if already_exist_insight_exists:
                    insight = already_exist_insight.first()
                    insight.content = content
                    insight.updated_at = timezone.now()
                    insight.save()
                else:
                    category = _categorize_insight(content)

                    insight = Insight.objects.create(
                        search_word=search_word,
                        category=category,
                        content=content,
                        source_url=template.link,
                    )

                insights.append(
                    {
                        "id": insight.id,
                        "search_word": insight.search_word,
                        "category": insight.category,
                        "content": insight.content,
                        "source_url": insight.source_url,
                    }
                )

            except Exception as e:
                print(f"Error processing template {template}: {e}")
                continue

    return insights


@shared_task
def daily_insight_collection(num: int = 5) -> List[dict]:
    """
    매일 실행되어 활성화된 모든 검색어에 대해 인사이트를 수집합니다.
    """
    keywords = SearchKeyword.objects.filter(is_active=True)
    results = []

    for keyword in keywords:
        try:
            insights = get_infos(keyword.keyword, num=num)
            keyword.last_searched_at = timezone.now()
            keyword.save()

            results.append(
                {
                    "keyword": keyword.keyword,
                    "insights_count": len(insights),
                    "status": "success",
                }
            )
        except Exception as e:
            results.append(
                {"keyword": keyword.keyword, "error": str(e), "status": "error"}
            )

    return results


@shared_task
def process_insights_to_structured_info():
    """수집된 인사이트를 구조화된 정보로 변환"""
    processor = InfoProcessor()

    # 비자 정보 처리
    visa_data_list = processor.process_visa_info()
    for visa_data in visa_data_list:
        try:
            VisaInfo.objects.update_or_create(
                visa_type=visa_data["visa_type"],
                defaults={
                    "requirements": visa_data["requirements"],
                    "process": visa_data["process"],
                    "duration": visa_data["duration"],
                },
            )
        except KeyError as e:
            print(f"Error processing visa data: {e}")
            continue

    # 문화 정보 처리
    culture_data_list = processor.process_culture_info()
    for culture_data in culture_data_list:
        try:
            CultureInfo.objects.create(
                culture_type=culture_data["culture_type"],
                title=culture_data["title"],
                content=culture_data["content"],
                tags=culture_data["tags"],
                source_urls=culture_data["source_urls"],
            )
        except KeyError as e:
            print(f"Error processing culture data: {e}")
            continue

    # 산업 정보 처리
    industry_data_list = processor.process_industry_info()
    for industry_data in industry_data_list:
        try:
            IndustryInfo.objects.create(
                industry_type=industry_data["industry_type"],
                description=industry_data["description"],
                trends=industry_data["trends"],
                opportunities=industry_data["opportunities"],
            )
        except KeyError as e:
            print(f"Error processing industry data: {e}")
            continue
