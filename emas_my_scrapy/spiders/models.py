from sqlite3 import Timestamp
from emas_my_scrapy.spiders.product_group import ProductGroup
from peewee import *

db = SqliteDatabase('gold_my.db')


class ProductGroupModel(Model):
    timestamp = CharField()

    class Meta:
        database = db
        table_name = None

# ------------------------------------------------------------------------------
# Maybank
# ------------------------------------------------------------------------------


class MaybankProductGroupModel(ProductGroupModel):
    pass


class MaybankGoldBullionModel(MaybankProductGroupModel):
    size = TextField()
    selling_rm = TextField()
    buying_rm = TextField()


class MaybankPaperProductGroupModel(MaybankProductGroupModel):
    selling_rm_per_gram = TextField()
    buying_rm_per_gram = TextField()


class MaybankGoldInvestmentAccountModel(MaybankPaperProductGroupModel):
    pass


class MaybankSilverInvestmentAccountModel(MaybankPaperProductGroupModel):
    pass


MaybankGoldBullionModel._meta.table_name = 'MAYBANK_GOLD_BULLION'
MaybankGoldInvestmentAccountModel._meta.table_name = 'MAYBANK_GOLD_INVESTMENT_ACCOUNT'
MaybankSilverInvestmentAccountModel._meta.table_name = 'MAYBANK_SILVER_INVESTMENT_ACCOUNT'

# ------------------------------------------------------------------------------
# Public Gold
# ------------------------------------------------------------------------------


class PGProductGroupModel(ProductGroupModel):
    weight = TextField()
    pg_sell = TextField()
    pg_buy = TextField()


class PGGoldBar24KModel(PGProductGroupModel):
    pass


class PGGoldGoldWaferDinar24KModel(PGProductGroupModel):
    pass


PGGoldBar24KModel._meta.table_name = 'PUBLIC_GOLD_GOLD_BAR_24K'
PGGoldGoldWaferDinar24KModel.table_name = 'PUBLIC_GOLD_GOLD_WAFER_DINAR_24K'

db.connect()
db.create_tables([
    MaybankGoldBullionModel,
    MaybankGoldInvestmentAccountModel,
    MaybankSilverInvestmentAccountModel,
    PGGoldBar24KModel,
    PGGoldGoldWaferDinar24KModel,
])
