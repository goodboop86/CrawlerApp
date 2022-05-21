from pydantic import BaseModel, Field, HttpUrl, validator
from typing import Union
#from model.crawler_model import CrawlDomain, CrawlType


class CrawlDomain(BaseModel):
    required: list[str] = ["baseshop"]


class CrawlType(BaseModel):
    required: list[str] = ["item_from_itempage", "items_from_itempagelist",
                           "item_from_toppage", "itemurls_from_sitemap"]


class Strategy(BaseModel):
    crawl_domain: str = Field(..., description='クロールするドメイン')
    crawl_type: str = Field(..., description='クロールする種類')

    @validator("crawl_domain")
    def crawl_target_validator(cls, v):
        domains = CrawlDomain.schema()["properties"]["required"]["default"]
        if v not in domains:
            raise ValueError(f"Should conatin {domains}.")
        return v

    @validator("crawl_type")
    def crawl_type_validator(cls, v):
        types = CrawlType.schema()["properties"]["required"]["default"]
        if v not in types:
            raise ValueError(f"Should conatin {types}.")
        return v


class CrawlRequest(BaseModel):
    target: Union[list[HttpUrl], HttpUrl] = Field(...)
    strategy: Strategy
