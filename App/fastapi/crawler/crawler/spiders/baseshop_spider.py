import scrapy
import json
import requests
from scrapy import Selector


class BaseshopSpider(scrapy.Spider):
    name = "baseshop"
    custom_settings = {'DOWNLOD_DELAY': 1}

    def __init__(self, url=None):
        self.url = url

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        tags: list[str] = response.xpath("//meta[@property]").getall()
        tags: list[Selector] = list(map(lambda x: Selector(text=x), tags))
        tags: list[list[str, str]] = list(map(lambda x: [x.xpath(
            "//meta/@property").get(), x.xpath("//meta/@content").get()], links))
        tags: dict = {k: v for k, v in tags}

        print(tags)

        with open(requests.utils.quote(self.url), 'w') as f:
            json.dump(tags, f)
