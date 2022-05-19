from enum import Enum
from crawler.baseshop_crawler import BaseShopCrawler
from model import crawler_model


class CrawlerFactory(object):
    def __init__(self, crawl_domain, crawl_type) -> None:
        self.__crawlers = {
            ""
        }
