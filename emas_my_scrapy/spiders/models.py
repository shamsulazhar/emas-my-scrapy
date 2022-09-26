from sqlite3 import Timestamp
from peewee import *

db = SqliteDatabase('gold_my.db')


class MaybankGoldBullionModel(Model):
    timestamp = CharField()
    size = TextField()
    selling_rm = TextField()
    buying_rm = TextField()

    class Meta:
        database = db
        table_name = 'MAYBANK_GOLD_BULLION'


db.connect()
db.create_tables([MaybankGoldBullionModel])
