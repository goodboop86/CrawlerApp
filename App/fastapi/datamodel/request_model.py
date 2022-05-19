from pydantic import BaseModel, Field, HttpUrl, validator
from typing import Union
from model.crawler_model import CrawlDomain, CrawlType


class Strategy(BaseModel):
    crawl_domain: str = Field(..., description='クロールするドメイン')
    crawl_type: str = Field(..., description='クロールする種類')

    @validator("crawl_domain")
    def crawl_target_validator(cls, v):
        values = [e.name for e in CrawlDomain]
        if v not in values:
            raise ValueError(f"Should conatin {values}.")
        return v

    @validator("crawl_type")
    def crawl_type_validator(cls, v):
        values = [e.name for e in CrawlType]
        if v not in values:
            raise ValueError(f"Should conatin {values}.")
        return v


class CrawlRequest(BaseModel):
    target: Union[list[HttpUrl], HttpUrl] = Field(...)
    strategy: Strategy
