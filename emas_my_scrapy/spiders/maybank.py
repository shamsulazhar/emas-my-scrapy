from datetime import datetime
from emas_my_scrapy.spiders.vendor import Vendor
from emas_my_scrapy.spiders.product_group import ProductGroup
from emas_my_scrapy.spiders.models import *


class MaybankProductGroup(ProductGroup):
    pass


class MaybankGoldBullion(MaybankProductGroup):
    model = MaybankGoldBullionModel

    def __init__(self, timestamp, data):
        super().__init__()

        self.timestamp = timestamp
        self.size = data[0]
        self.selling_rm = data[1]
        self.buying_rm = data[2]

    def __str__(self) -> str:
        return super().__str__() + f'size: {self.model.size}\nselling_rm: {self.model.selling_rm}\nbuying_rm: {self.model.buying_rm}'

    def create_model(self):
        self.model = MaybankGoldBullion.model.create(
            timestamp=self.timestamp,
            size=self.size,
            selling_rm=self.selling_rm,
            buying_rm=self.buying_rm
        )

    def is_unique(self):
        table = MaybankGoldBullion.model

        results = table.select().where(
            (table.timestamp == self.timestamp) & (table.size == self.size))

        return len(results) == 0

    @classmethod
    def extract_date_time_from_node(cls, response):
        raw_date_time_str = response.xpath(
            '//*[@id="iw_comp1542994945699"]/div/section/main/div/article[2]/section/div/section/div/div[1]/div[2]/p//text()').get()

        return datetime.strptime(raw_date_time_str, 'Effective on %d %b %Y %I:%M %p')

    @classmethod
    def get_price_table_node(cls, response):
        return response.xpath('//*[@id="iw_comp1542994945699"]/div/section/main/div/article[2]/section/div/section/div/div[1]/div[2]/table')

    @classmethod
    def check_header(cls, header_nodes):
        assert header_nodes[0].xpath('text()').get() == 'Size (oz)'
        assert header_nodes[1].xpath('text()').get() == 'Selling (RM)'
        assert header_nodes[2].xpath('text()').get() == 'Buying (RM)'

    @classmethod
    def all_but_header(cls, table_node):
        tds = table_node.xpath('.//td')

        table = []
        row = None
        for i in range(len(tds)):
            mod_three = i % 3
            if mod_three == 0:
                row = []

            data = tds[i].xpath('text()').get()
            row.append(data)

            if mod_three == 2:
                table.append(row)

        return table


class MaybankPaperProductGroup(MaybankProductGroup):
    pass


class MaybankGoldInvestmentAccount(MaybankPaperProductGroup):
    pass


class MaybankSilverInvestmentAccount(MaybankPaperProductGroup):
    pass


class Maybank(Vendor):
    url = 'https://www.maybank2u.com.my/maybank2u/malaysia/en/personal/rates/gold_and_silver.page'
    product_groups = [
        # MaybankSilverInvestmentAccount(),
        # MaybankGoldInvestmentAccount(),
        MaybankGoldBullion
    ]

    def get_product_groups(self):
        return Maybank.product_groups
