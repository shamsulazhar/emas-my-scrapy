import scrapy
from emas_my_scrapy.spiders.maybank import Maybank
from emas_my_scrapy.spiders.pg import PG
from emas_my_scrapy.spiders.uob import UOB


class EmasMy(scrapy.Spider):
    name = 'emas_my'
    vendors = [
        Maybank(),
        # PG(),
        UOB()
    ]

    def start_requests(self):

        for vendor in EmasMy.vendors:
            print(
                f'vendor.url(): {vendor.url} - vendor.parse: {vendor.parse}')

            yield scrapy.Request(url=vendor.url, callback=vendor.parse)
