# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class EmasMyScrapyPipeline:
    # def __init__(self) -> None:
    #     self.con = sqlite3.connect('gold_my.db')
    #     self.cur = self.con.cursor

    # def create_table(self):

    def process_item(self, item, spider):
        for product_group_list in item.values():
            for product_group_item in product_group_list:
                print('^' * 80)
                print(f'item: {product_group_item}')
                product_group_item.save_if_unique()

        return item
