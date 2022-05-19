from enum import Enum
from typing import Union

from pydantic import HttpUrl
from crawler.baseshop_crawler import BaseShopCrawler
from model import crawler_model
from datamodel.request_model import CrawlRequest


class CrawlerFactory(object):
    def __init__(self, request: CrawlRequest) -> None:
        target: Union[list[HttpUrl], HttpUrl] = request.target
        crawl_domain: str = request.strategy.crawl_domain
        crawl_type: str = request.strategy.crawl_type

        self.__cls = globals(crawl_domain)
        self.__func = getattr(self.__cls, crawl_type)
        self.__cls.__init__(target=target, func=self.__func)

        return self.__cls
