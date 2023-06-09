from datetime import datetime
import dateparser
from emas_my_scrapy.spiders.vendor import Vendor
from emas_my_scrapy.spiders.product_group import ProductGroup
from emas_my_scrapy.spiders.models import *


class PGHeaderWithWeight:
    @classmethod
    def check_header(cls, header_nodes):
        assert header_nodes[0].xpath('./p/text()').get() == 'Weight'
        super().check_header(header_nodes)


def init_buy_sell_data(self, data):
    self.pg_sell = data[1]
    self.pg_buy = data[2]


def check_table_rowcount_and_test_cell(table, expected_rows, test_cell_xpath, expected_test_cell_value):
    rows = table.xpath('.//tr')
    return len(rows) == expected_rows and (table.xpath(test_cell_xpath).get() == expected_test_cell_value)


class PGProductGroup(ProductGroup):
    def __init__(self, timestamp, data) -> None:
        super().__init__(timestamp)

        self.weight = data[0]

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

    @classmethod
    def extract_date_time_from_node(cls, response):
        raw_date_time_str = response.xpath(
            '//*[@id="red-table2"]/b[not(contains(@style, "display:none;"))]//font//text()').get()
        timestamp = dateparser.parse(raw_date_time_str[12:-1])
        assert isinstance(timestamp, datetime)

        return timestamp

    @classmethod
    def check_header(cls, header_nodes):
        assert header_nodes[1].xpath('./p/text()').get() == 'PG Sell (RM)'
        assert header_nodes[2].xpath('./p/text()').get() == 'PG Buy (RM)'

    @classmethod
    def all_but_header(cls, table_node):
        rows = table_node.xpath('.//tr')[1:]
        table = []
        for row in rows:
            table.append(row.xpath('.//td//p//text()').getall())

        return table


class PGGoldBar24K(PGProductGroup,  PGHeaderWithWeight):
    model = PGGoldBar24KModel

    def __init__(self, timestamp, data) -> None:
        super().__init__(timestamp, data)

        init_buy_sell_data(self, data)

    @classmethod
    def table_test(cls, table):
        return check_table_rowcount_and_test_cell(table, 7, './tr[7]/td[1]//a/text()', '1000 gram')


class PGGoldGoldWaferDinar24K(PGProductGroup):
    model = PGGoldGoldWaferDinar24KModel

    def __init__(self, timestamp, data) -> None:
        super().__init__(timestamp, data)

        init_buy_sell_data(self, data)

    @classmethod
    def check_header(cls, header_nodes):
        assert header_nodes[0].xpath('./p/text()').get() == 'Dinar'
        super().check_header(header_nodes)

    @classmethod
    def table_test(cls, table):
        return check_table_rowcount_and_test_cell(table, 4, './/tr[4]/td[1]//a/text()', '10 Dinar')


class PGGoldSmallBarWafer24K(PGProductGroup):
    model = PGGoldSmallBarWafer24KModel

    def __init__(self, timestamp, data) -> None:
        super().__init__(timestamp, data)

        self.pg_sell = data[1]

    def create_model(self):
        self.model = self.__class__.model.create(
            timestamp=self.timestamp,
            weight=self.weight,
            pg_sell=self.pg_sell,
        )

    @classmethod
    def check_header(cls, header_nodes):
        print('header nodes: ' + str(header_nodes[0].get()))
        assert header_nodes[0].xpath('./p/text()').get() == 'Weight'
        assert header_nodes[1].xpath('./p/text()').get() == 'PG Sell (RM)'

    @classmethod
    def table_test(cls, table):
        return check_table_rowcount_and_test_cell(table, 5, './/tr[4]/td[1]//p//a/text()', '1/2 Dinar')


class PGClassicBungamasTaiFook24K(PGProductGroup, PGHeaderWithWeight):
    model = PGClassicBungamasTaiFook24KModel

    def __init__(self, timestamp, data) -> None:
        super().__init__(timestamp, data)

        init_buy_sell_data(self, data)

    @classmethod
    def table_test(cls, table):
        return check_table_rowcount_and_test_cell(table, 5, './/tr[5]/td[1]//a/text()', '100 gram')


class PGFlexibar24K(PGProductGroup, PGHeaderWithWeight):
    model = PGFlexibar24KModel

    def __init__(self, timestamp, data) -> None:
        super().__init__(timestamp, data)

        init_buy_sell_data(self, data)

    @classmethod
    def table_test(cls, table):
        return check_table_rowcount_and_test_cell(table, 2, './/tr[2]//td[1]/p/text()', '50 gram')


class PGGoldGoldWaferDinar22K(PGProductGroup):
    model = PGGoldGoldWaferDinar22KModel

    def __init__(self, timestamp, data) -> None:
        super().__init__(timestamp, data)

        init_buy_sell_data(self, data)

    @classmethod
    def check_header(cls, header_nodes):
        assert header_nodes[0].xpath('./p/text()').get() == 'Dinar'
        super().check_header(header_nodes)

    @classmethod
    def table_test(cls, table):
        return check_table_rowcount_and_test_cell(table, 2, './tr/td[1]/p/text()', '1 Dinar')


class PGGoldJewellery22K(PGProductGroup):
    model = PGGoldJewellery22KModel

    def __init__(self, timestamp, data) -> None:
        super().__init__(timestamp, data)

        self.pg_buy = data[1]

    def create_model(self):
        self.model = self.__class__.model.create(
            timestamp=self.timestamp,
            weight=self.weight,
            pg_buy=self.pg_buy
        )

    @classmethod
    def check_header(cls, header_nodes):
        assert header_nodes[0].xpath('./p/text()').get() == 'Weight'
        assert header_nodes[1].xpath('./p/text()').get() == 'PG Buy (RM)'

    @classmethod
    def table_test(cls, table):
        return check_table_rowcount_and_test_cell(table, 2, './tr/td[1]/p/text()', '1 gram')


class PGSilverBullion(PGProductGroup, PGHeaderWithWeight):
    model = PGSilverBullionModel

    def __init__(self, timestamp, data) -> None:
        super().__init__(timestamp, data)

        init_buy_sell_data(self, data)

    @classmethod
    def table_test(cls, table):
        return check_table_rowcount_and_test_cell(table, 6, './/tr[6]/td[1]/p//text()', '5 kilogram')


class PGSilverWaferDirham(PGProductGroup, PGHeaderWithWeight):
    model = PGSilverWaferDirhamModel

    def __init__(self, timestamp, data) -> None:
        super().__init__(timestamp, data)

        init_buy_sell_data(self, data)

    @classmethod
    def table_test(cls, table):
        return check_table_rowcount_and_test_cell(table, 2, './/tr[2]/td[1]/p//text()', '10 Dirham')


class PG(Vendor):
    url = 'https://publicgold.com.my/'
    product_groups = [
        PGGoldBar24K,
        PGGoldGoldWaferDinar24K,
        PGGoldSmallBarWafer24K,
        PGClassicBungamasTaiFook24K,
        PGFlexibar24K,
        PGGoldGoldWaferDinar22K,
        PGGoldJewellery22K,
        PGSilverBullion,
        PGSilverWaferDirham
    ]
