from datetime import datetime
import dateparser
import csv
from io import StringIO
from emas_my_scrapy.spiders.vendor import Vendor
from emas_my_scrapy.spiders.product_group import ProductGroup
from emas_my_scrapy.spiders.models import *


class UOBGoldBullion(ProductGroup):
    model = UOBGoldBullionModel

    def __init__(self, timestamp, data) -> None:
        super().__init__(timestamp)

        self.weight = data[0]
        self.gold_type = data[1]
        self.wm_bank_selling_rm = data[2]
        self.em_bank_selling_rm = data[3]
        self.bank_buying = data[4]

    def create_model(self):
        self.model = self.__class__.model.create(
            timestamp=self.timestamp,
            weight=self.weight,
            gold_type=self.gold_type,
            wm_bank_selling_rm=self.wm_bank_selling_rm,
            bank_buying=self.bank_buying,
            em_bank_selling_rm=self.em_bank_selling_rm,
        )

    def uniqueness_test(self, table):
        return table.select().where(
            (table.timestamp == self.timestamp) & (table.weight == self.weight) & (table.gold_type == self.gold_type))

    @classmethod
    def extract_data_from_root_node(cls, response):
        f = StringIO(response.text)
        reader = csv.reader(f, delimiter=',')

        price_table = []
        for row in reader:
            price_table.append(row)

        # Drop the header
        price_table.pop(0)

        def create_product(data_row):
            date_time = data_row[-1]
            timestamp = dateparser.parse(date_time)
            assert isinstance(timestamp, datetime)

            return cls(timestamp, data_row)

        return list(map(create_product, price_table))


class UOB(Vendor):
    # url = 'https://www.uob.com.my/online-rates/gold-bullion-prices.page'
    url = 'https://www.uob.com.my/wsm/stayinformed.do?path=gold2'
    product_groups = [
        UOBGoldBullion
    ]
