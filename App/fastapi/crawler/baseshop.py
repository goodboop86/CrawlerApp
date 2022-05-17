
from fastapi import FastAPI
from pydantic import BaseModel
from lxml import html
import requests


class BaseShop:
    def __init__(self, url):
        self.url = url

    def crawl(self):
        res = requests.get(self.url)
        tree = html.fromstring(res.text)
        childs: list[html.HtmlElement] = tree.xpath("//meta[@property]")
        childs: list[list[str, str]] = list(map(lambda x: x.values(), childs))

        tags: dict[str, str] = {k.replace(':', '_'): v for k, v in childs}

        return tags
