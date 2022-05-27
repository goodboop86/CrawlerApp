# -*- coding: utf-8 -*-


import uvicorn
from crawler.crawler_factory import CrawlerFactory
from fastapi import FastAPI
from datamodel.baseshop_model import Shop, Item
from datamodel.request_model import CrawlRequest, CrawlDomain, AuthRequest
from typing import Union
from auth.auth import Auth


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/crawl", response_model=Union[Item, Shop])
async def crawl(request: CrawlRequest):
    crawler = CrawlerFactory(request=request)
    result = crawler()
    return result


@app.post("/signup")
async def signup(request: AuthRequest):
    auth = Auth()
    response = auth.signup(request.username, request.password)
    return response


@app.post("/signin",)
async def signin(request: AuthRequest):
    auth = Auth()
    response = auth.signin(request.username, request.password)
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
