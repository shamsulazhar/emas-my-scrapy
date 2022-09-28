from datetime import datetime
import dateparser
from emas_my_scrapy.spiders.vendor import Vendor
from emas_my_scrapy.spiders.product_group import ProductGroup
from emas_my_scrapy.spiders.models import *


class PGProductGroup(ProductGroup):
    def __init__(self, timestamp, data) -> None:
        super().__init__(timestamp)

        self.weight = data[0]
        self.pg_sell = data[1]
        self.pg_buy = data[2]

    def create_model(self):
        self.model = self.__class__.model.create(
            timestamp=self.timestamp,
            weight=self.weight,
            pg_sell=self.pg_sell,
            pg_buy=self.pg_buy
        )

    def uniqueness_test(self, table):
        return table.select().where(
            (table.timestamp == self.timestamp) & (table.weight == self.weight))

    @classmethod
    def get_price_table_node(cls, response):
        # Get all tables from the response
        tables = response.xpath('//table')

        # Find the table of interest
        for table in tables:
            if cls.table_test(table):
                break

        return table


class PGGoldBar24K(PGProductGroup):
    model = PGGoldBar24KModel

    @classmethod
    def extract_date_time_from_node(cls, response):
        raw_date_time_str = response.xpath(
            '//*[@id="red-table2"]/b[not(contains(@style, "display:none;"))]//font//text()').get()
        timestamp = dateparser.parse(raw_date_time_str[12:-1])
        assert isinstance(timestamp, datetime)

        return timestamp

    @classmethod
    def table_test(cls, table):
        rows = table.xpath('.//tr')
        return len(rows) == 7 and (table.xpath('./tr[7]/td[1]//a/text()').get() == '1000 gram')

    @classmethod
    def check_header(cls, header_nodes):
        assert header_nodes[0].xpath('./p/text()').get() == 'Weight'
        assert header_nodes[1].xpath('./p/text()').get() == 'PG Sell (RM)'
        assert header_nodes[2].xpath('./p/text()').get() == 'PG Buy (RM)'

    @classmethod
    def all_but_header(cls, table_node):
        rows = table_node.xpath('.//tr')[1:]
        table = []
        for row in rows:
            table.append(row.xpath('.//td//p//text()').getall())

        return table


class PG(Vendor):
    url = 'https://publicgold.com.my/'
    product_groups = [
        PGGoldBar24K
    ]
