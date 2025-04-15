import httpx

from common.errors import CrawlError


class BaseCrawler(object):
    """
    Base class for crawlers.
    """
    async def crawl_async(self, url, client):
        """
        비동기로 URL을 크롤링합니다.
        :param url:
        :param client:
        :return:
        """
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            raise CrawlError(f"Error fetching {url}: {e}") from e