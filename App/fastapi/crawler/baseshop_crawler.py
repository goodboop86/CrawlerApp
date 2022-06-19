
from lxml import html
from crawler.crawler import Crawler
import requests
from pydantic import HttpUrl
from typing import Callable
from schema.request_model import CrawlRequest


class BaseShopCrawler(Crawler):

    def __init__(self, target: HttpUrl, func: Callable):

        self.__target: HttpUrl = target
        self.__crawl_func: Callable = func

    def __call__(self):
        return self.__crawl_func(target=self.__target)

    @staticmethod
    def _item_from_itempage(target: HttpUrl):
        res = requests.get(target)
        tree = html.fromstring(res.text)
        childs: list[html.HtmlElement] = tree.xpath("//meta[@property]")
        childs: list[list[str, str]] = list(map(lambda x: x.values(), childs))
        tags: dict[str, str] = {k.replace(':', '_'): v for k, v in childs}

        return tags

    @staticmethod
    def _items_from_itempagelist(target: list[HttpUrl]):
        pass

    @staticmethod
    def _item_from_toppage(target: HttpUrl):
        res = requests.get(target)
        tree = html.fromstring(res.text)
        childs: list[html.HtmlElement] = tree.xpath("//meta[@property]")
        childs: list[list[str, str]] = list(map(lambda x: x.values(), childs))
        tags: dict[str, str] = {k.replace(':', '_'): v for k, v in childs}

        return tags

    @staticmethod
    def _itemurls_from_sitemap(target: HttpUrl):
        pass
