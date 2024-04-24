from typing import Iterable
import scrapy
from pathlib import Path
from fake_useragent import UserAgent


ua = UserAgent()


class OzonSpider(scrapy.Spider):
    name = "ozon"

    def start_requests(self):
        urls = ["https://www.ozon.ru/category/smartfony-15502/?sorting=rating"]

        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                headers={"User-Agent": ua.chrome},
                
            )

    def parse(self, response):
        print("response", response)
        # page = response.url.split("/")[-2]
        # filename = f"quotes-{page}.html"
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")
