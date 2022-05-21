# -*- coding: utf-8 -*-


import uvicorn
from crawler.crawler_factory import CrawlerFactory
from fastapi import FastAPI
from datamodel.baseshop_model import Shop, Item
from datamodel.request_model import CrawlRequest, CrawlDomain
from typing import Union


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/crawl", response_model=Union[Item, Shop])
async def post(request: CrawlRequest):
    crawler = CrawlerFactory(request=request)
    result = crawler()
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
