import scrapy
import store
import product
from urllib.parse import urlencode


class Spider(scrapy.Spider):
    name = "products"

    def start_requests(self):
        yield scrapy.Request(
            "https://store-data-service.services.dmtech.com/sitemap/DE",
            self.parse_stores,
        )
        yield scrapy.Request(
            "https://products.dm.de/productfeed/DE/sitemap.xml",
            self.parse_products,
        )

    def parse_products_detail(self, response):
        print(response.json()[0]["name"])

    def parse_products(self, response):
        response.selector.remove_namespaces()
        for product_url in response.css("loc::text").getall()[0:5]:
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

    def parse_stores(self, response):
        response.selector.remove_namespaces()
        for store_url in response.css("loc::text").getall()[0:5]:
            match = store.match_from_url(store_url)
            if match:
                print(store_url, match)

    def parse(self, response):
        for h3 in response.xpath("//h3").getall():
            yield MyItem(title=h3)

        for href in response.xpath("//a/@href").getall():
            yield scrapy.Request(response.urljoin(href), self.parse)
