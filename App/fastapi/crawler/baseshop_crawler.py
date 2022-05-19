
from lxml import html
from datamodel.request_model import CrawlRequest, CrawlType
from crawler.crawler import Crawler
import requests
from pydantic import HttpUrl
from typing import Callable


class BaseShopCrawler(Crawler):

    def __init__(self, target: HttpUrl, func: Callable):

        self.__target: HttpUrl = target
        self.__crawl_func: Callable = func

    def __call__(self):
        self.__crawl_func()

    def __item(self):
        return self.__shop()

    def __shop(self):
        res = requests.get(self.__target)
        tree = html.fromstring(res.text)
        childs: list[html.HtmlElement] = tree.xpath("//meta[@property]")
        childs: list[list[str, str]] = list(map(lambda x: x.values(), childs))
        tags: dict[str, str] = {k.replace(':', '_'): v for k, v in childs}

        return tags

    def __crawl_list(self):
        pass

    def __item_list(self):
        pass

    def crawl_item(self):
        res = requests.get(self.target)
        tree = html.fromstring(res.text)
        childs: list[html.HtmlElement] = tree.xpath("//meta[@property]")
        childs: list[list[str, str]] = list(map(lambda x: x.values(), childs))

        tags: dict[str, str] = {k.replace(':', '_'): v for k, v in childs}

        return tags
