import jsonlines
import itertools
import datetime
import scrapy
import os
from scrapy.item import Item, Field


class AvailabilityItem(Item):
    date = Field()
    country = Field()
    product = Field()
    store = Field()
    stock = Field()


class AvalabilitySpider(scrapy.Spider):
    name = "availability"
    date = datetime.date.today().isoformat()
    root = os.path.dirname(__file__)

    custom_settings = {
        # "JOBDIR": "/app/jobs/availability/",
        # "DOWNLOAD_DELAY": 0.25,
        "FEEDS": {
            "file://"
            + root
            + "/data/%(name)s/%(date)s.jsonl.gz": {
                "format": "jsonlines",
                "postprocessing": ["scrapy.extensions.postprocessing.GzipPlugin"],
                "gzip_compresslevel": 5,
            },
        },
    }

    def start_requests(self):
        with jsonlines.open("stores.jsonl") as reader:
            stores = [obj["id"] for obj in reader]

        with jsonlines.open("products.jsonl") as reader:
            products = [obj["dan"] for obj in reader]

        chunk_size = 10
        chunked_stores = [
            stores[i : i + chunk_size] for i in range(0, len(stores), chunk_size)
        ]
        chunked_products = [
            products[i : i + chunk_size] for i in range(0, len(products), chunk_size)
        ]

        for stores in chunked_stores:
            for products in chunked_stores:
                yield scrapy.Request(
                    "https://products.dm.de/store-availability/%s/availability?dans=%s&storeNumbers=%s"
                    % ("de", ",".join(map(str, products)), ",".join(map(str, stores))),
                    self.parse_availability,
                )

        """
        for stores in chunked_stores:
            print(stores)
            for url in [
                "https://products.dm.de/store-availability/%s/products/dans/%d/availability-with-listing?storeNumbers=%s"
                % ("DE", product, ",".join(map(str, stores)))
                for product in products
            ]:
                yield scrapy.Request(url, self.parse_availability)
        """

    def parse_availability(self, response):
        record = response.json()
        for availability in list(
            itertools.chain(*record["storeAvailabilities"].values())
        ):
            yield AvailabilityItem(
                date=datetime.datetime.now().isoformat(),
                country=record["tenant"].upper(),
                product=availability["dan"],
                store=availability["store"]["storeNumber"],
                stock=availability.get("stockLevel", None),
            )

    def OLD_parse_availability(self, response):
        record = response.json()
        for availability in record["storeAvailability"]:
            print(availability)
            yield AvailabilityItem(
                date=datetime.datetime.now().isoformat(),
                country=record["tenant"],
                product=record["dan"],
                store=availability["store"]["storeNumber"],
                stock=availability.get("stockLevel", None),
            )
