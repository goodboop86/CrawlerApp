# -*- coding: utf-8 -*-


from crawler.baseshop import BaseShop
from fastapi import FastAPI
from pydantic import BaseModel
from model.baseshop import Shop, Item
from model.request import ScrapeTarget
from typing import Union
import requests

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/post", response_model=Union[Item, Shop])
async def post(request: ScrapeTarget):
    url = requests.utils.unquote(request.target)

    if url is None:
        return {"200": "入力してください。\n 例:https://reo.thebase.in/items/6019347 https://reo.thebase.in/"}

    crawler = BaseShop(url=url)

    return crawler.crawl()
