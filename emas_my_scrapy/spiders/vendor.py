class Vendor:
    def parse(self, response):
        for product_group in self.get_product_groups():
            product_data_table = product_group.extract_data_from_root_node(
                response)

            yield {product_group.get_table_name(): product_data_table}
