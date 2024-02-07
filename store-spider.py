import scrapy
import store
from scrapy.item import Item, Field


class StoreItem(Item):
    country = Field()
    id = Field()


class StoreSpider(scrapy.Spider):
    name = "stores"

    custom_settings = {
        "FEEDS": {
            "file:///app/%(name)s.jsonl": {"format": "jsonlines", "overwrite": True},
        },
    }

    def start_requests(self):
        yield scrapy.Request(
            "https://store-data-service.services.dmtech.com/sitemap/DE",
            self.parse_stores,
        )

    def parse_stores(self, response):
        response.selector.remove_namespaces()
        for store_url in response.css("loc::text").getall():
            match = store.match_from_url(store_url)
            if match:
                print(store_url, match)
                yield StoreItem(country=match[0], id=match[1])
