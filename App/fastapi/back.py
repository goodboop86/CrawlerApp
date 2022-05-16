# -*- coding: utf-8 -*-

from fastapi import FastAPI
from pydantic import BaseModel
from lxml import html
import lxml
import json
import time
#import scrapy
import requests
from urllib3 import request
from bs4 import BeautifulSoup
from scrapy import Selector

app = FastAPI()


class ScrapeTarget(BaseModel):
    target: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/post")
async def post(request: ScrapeTarget):
    def on_changed(event):
        print("################# changed")

        with open(json_name, "r") as f:
            tags = json.load(f)
        return tags

    if request.target is None:
        return {"pass": "200"}

    url = requests.utils.unquote(request.target)
    print(url)

    res = requests.get(url)
    tree = lxml.html.fromstring(res.text)
    # req = requests.get(url)
    # parser = lxml.html.HTMLParser(encoding='utf-8')
    # tree = lxml.html.parse(url)
    # soup: BeautifulSoup = BeautifulSoup(req.text, "html.parser")
    # root: html.HtmlElement = html.fromstring(str(soup))
    childs: list[html.HtmlElement] = tree.xpath("//meta[@property]")
    childs: list[list[str, str]] = list(map(lambda x: x.values(), childs))
    print(childs)
    tags: dict[str, str] = {v: k for v, k in childs}

    return tags
