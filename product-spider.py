import scrapy
import product
from scrapy.item import Item, Field


class ProductItem(Item):
    country = Field()
    dan = Field()
    gtin = Field()


class ProductSpider(scrapy.Spider):
    name = "products"

    custom_settings = {
        "FEEDS": {
            "file:///app/%(name)s.jsonl": {"format": "jsonlines", "overwrite": True},
        },
    }

    def start_requests(self):
        yield scrapy.Request(
            "https://products.dm.de/productfeed/DE/sitemap.xml",
            self.parse_products,
        )

    def parse_products_detail(self, response):
        record = response.json()[0]
        print(record["name"])
        yield ProductItem(
            country=record["isoCountry"], dan=record["dan"], gtin=record["gtin"]
        )

    def parse_products(self, response):
        response.selector.remove_namespaces()
        for product_url in response.css("loc::text").getall():
            match = product.match_from_url(product_url)
            if match:
                print(product_url, match)
                yield response.follow(
                    "https://products.dm.de/product/"
                    + match[0]
                    + "/products/gtins/"
                    + str(match[1]),
                    self.parse_products_detail,
                    # cb_kwargs={"game": game}
                )
