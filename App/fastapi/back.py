# -*- coding: utf-8 -*-


from crawler.baseshop_crawler import BaseShopCrawler
from crawler.crawler_factory import CrawlerFactory
from fastapi import FastAPI
from datamodel.baseshop_model import Shop, Item
from datamodel.request_model import CrawlRequest, CrawlDomain
from typing import Union


app = FastAPI()

crawl_target = {
    CrawlDomain.baseshop: BaseShopCrawler
}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/crawl", response_model=Union[Item, Shop])
async def post(request: CrawlRequest):

    crawler = CrawlerFactory(request=request)
    return crawler()
