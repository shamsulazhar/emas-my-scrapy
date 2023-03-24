class Vendor:
    def get_product_groups(self):
        return self.__class__.product_groups

    def parse(self, response):
        for product_group in self.get_product_groups():
            print('product group: ' + str(product_group))
            product_data_table = product_group.extract_data_from_root_node(
                response)

            yield {product_group.get_table_name(): product_data_table}
