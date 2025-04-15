import asyncio

from rest_framework.test import APITestCase

from .crawlers.google_crawler import GoogleCrawler


class InsightsTest(APITestCase):
    def test_google_crawling(self):
        google_crawling = GoogleCrawler()
        google_crawling_res = asyncio.run(google_crawling.google_crawl_async('hello world', num=10))
        self.assertEqual(
            len(google_crawling_res),
            10,
        )
        self.assertEqual(
            google_crawling_res[0].search_word,
            "hello world",
        )
        self.assertIn(
            "html",
            google_crawling_res[0].__dict__,
        )
