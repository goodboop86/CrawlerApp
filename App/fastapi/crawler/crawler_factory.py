from typing import Callable

from pydantic import HttpUrl
from datamodel.request_model import CrawlRequest
from factorymap.crawler_factorymap import CrawlDomainMap, CrawlTypeMap
from typing import Union


class CrawlerFactory(object):
    def __new__(self, request: CrawlRequest):
        target: Union[list[HttpUrl], HttpUrl] = request.target
        domain: str = request.strategy.crawl_domain
        type: str = request.strategy.crawl_type

        crawler: any = CrawlDomainMap[domain].value
        func: Callable = getattr(crawler, CrawlTypeMap[type].value)

        return crawler(target=target, func=func)
