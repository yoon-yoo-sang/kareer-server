import asyncio
import os
from dataclasses import dataclass

import httpx
from dotenv import load_dotenv

from insights.crawlers.base_crawler import BaseCrawler

load_dotenv()


@dataclass
class GoogleCrawlTemplate:
    search_word: str
    link: str
    html: str = ""

    def __repr__(self):
        return f"search_word: {self.search_word}, link: {self.link}\n"


class GoogleCrawler(BaseCrawler):
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Singleton pattern을 사용하여 GoogleCrawler의 인스턴스를 생성합니다.
        :param args:
        :param kwargs:
        """
        if cls._instance is None:
            cls._instance = super(GoogleCrawler, cls).__new__(cls)
            cls._instance.api_key = os.getenv("GOOGLE_API_KEY")
            cls._instance.search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
        return cls._instance

    async def google_crawl_async(self, query: str, **params) -> list[GoogleCrawlTemplate]:
        """
        Google Custom Search API를 사용하여 검색 결과를 가져오고,
        해당 링크를 크롤링합니다.
        :param query:
        :param params:
        :return:
        """
        google_response = await self.google_search_async(query, **params)
        links = self.get_links(google_response)

        crawl_templates = [GoogleCrawlTemplate(query, link, "") for link in links]

        async with httpx.AsyncClient() as client:
            tasks = [
                self.crawl_async(template.link, client) for template in crawl_templates
            ]
            html_results = await asyncio.gather(*tasks, return_exceptions=True)

        for template, html in zip(crawl_templates, html_results):
            if isinstance(html, Exception):
                template.html = ""
            else:
                template.html = html

        return crawl_templates

    def get_links(self, google_response: dict) -> list[str]:
        """
        Google Custom Search API의 응답에서 링크를 추출합니다.
        :param google_response:
        :return:
        """
        items = google_response['items']
        links = [item['link'] for item in items]
        return links

    async def google_search_async(self, query: str, **params) -> dict:
        """
        Google Custom Search API를 사용하여 검색 결과를 가져옵니다.
        :param query:
        :param params:
        :return:
        """
        base_url = 'https://www.googleapis.com/customsearch/v1'
        params = {
            'key': self.api_key,
            'cx': self.search_engine_id,
            'q': query,
            **params,
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(base_url, params=params)
            response.raise_for_status()
            return response.json()
