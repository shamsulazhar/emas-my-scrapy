from datetime import datetime


class ProductGroup:
    def __init__(self, timestamp) -> None:
        self.timestamp = timestamp

    def __str__(self) -> str:
        return f'time_stamp: {self.timestamp}\n'

    def save(self):
        self.model.save()

    def save_if_unique(self):
        if self.is_unique():
            self.create_model()
            self.save()

    def is_unique(self):
        table = self.__class__.model

        results = self.uniqueness_test(table)

        return len(results) == 0

    @classmethod
    def check_and_return_valid_date(cls, format_str, raw_date_time_str):
        timestamp = datetime.strptime(raw_date_time_str, format_str)

        assert datetime.strftime(timestamp, format_str) == raw_date_time_str

        return timestamp

    @classmethod
    def get_table_name(cls):
        return cls.model._meta.table_name

    @classmethod
    def extract_tables(cls, response):
        return response.xpath('//table')

    @classmethod
    def extract_header_from_table(cls, table_node):
        return table_node.xpath('.//th')

    @classmethod
    def extract_price_table_from_node(cls, response):
        # tables = cls.extract_tables(response)
        # key = cls.price_table_key(tables)
        table = cls.get_price_table_node(response)
        table_header = cls.extract_header_from_table(table)
        cls.check_header(table_header)

        return cls.all_but_header(table)

    @classmethod
    def extract_data_from_root_node(cls, response):
        date_time = cls.extract_date_time_from_node(response)

        price_table = cls.extract_price_table_from_node(response)

        def create_product(data_row):
            return cls(date_time, data_row)

        return list(map(create_product, price_table))
