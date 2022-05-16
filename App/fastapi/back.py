# -*- coding: utf-8 -*-

from fastapi import FastAPI
from pydantic import BaseModel
from lxml import html
import requests

app = FastAPI()


class ScrapeTarget(BaseModel):
    target: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/post")
async def post(request: ScrapeTarget):

    if request.target is None:
        return {"pass": "200"}

    url = requests.utils.unquote(request.target)

    res = requests.get(url)
    tree = html.fromstring(res.text)
    childs: list[html.HtmlElement] = tree.xpath("//meta[@property]")
    childs: list[list[str, str]] = list(map(lambda x: x.values(), childs))
    print(childs)
    tags: dict[str, str] = {v: k for v, k in childs}

    return tags
