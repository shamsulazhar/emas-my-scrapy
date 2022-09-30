from sqlite3 import Timestamp
from emas_my_scrapy.spiders.product_group import ProductGroup
from peewee import *

# db = SqliteDatabase('gold_my.db')
# db = MySQLDatabase('ab86864_MyGold', user='root', password='root', port=8889)
db = MySQLDatabase(
    'ab86864_MyGold',
    user='ab86864_MyGold',
    password='QQDqp@oCqoS`n2gH7o',
    port=5522
)


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


class PGGoldBar24KModel(PGProductGroupModel):
    pg_sell = TextField()
    pg_buy = TextField()


class PGGoldGoldWaferDinar24KModel(PGProductGroupModel):
    pg_sell = TextField()
    pg_buy = TextField()


class PGGoldSmallBarWafer24KModel(PGProductGroupModel):
    pg_sell = TextField()


class PGClassicBungamasTaiFook24KModel(PGProductGroupModel):
    pg_sell = TextField()
    pg_buy = TextField()


class PGFlexibar24KModel(PGProductGroupModel):
    pg_sell = TextField()
    pg_buy = TextField()


class PGGoldGoldWaferDinar22KModel(PGProductGroupModel):
    pg_sell = TextField()
    pg_buy = TextField()


class PGGoldJewellery22KModel(PGProductGroupModel):
    pg_buy = TextField()


class PGSilverBullionModel(PGProductGroupModel):
    pg_sell = TextField()
    pg_buy = TextField()


class PGSilverWaferDirhamModel(PGProductGroupModel):
    pg_sell = TextField()
    pg_buy = TextField()


PGGoldBar24KModel._meta.table_name = 'PUBLIC_GOLD_GOLD_BAR_24K'
PGGoldGoldWaferDinar24KModel._meta.table_name = 'PUBLIC_GOLD_GOLD_WAFER_DINAR_24K'
PGGoldSmallBarWafer24KModel._meta.table_name = 'PUBLIC_GOLD_SMALL_BAR_WAFER_24K'
PGClassicBungamasTaiFook24KModel._meta.table_name = 'PUBLIC_GOLD_CLASSIC_BUNGAMAS_TAI_FOOK_24K'
PGFlexibar24KModel._meta.table_name = 'PUBLIC_GOLD_FLEXIBAR_24K'
PGGoldGoldWaferDinar22KModel._meta.table_name = 'PUBLIC_GOLD_GOLD_WAFER_DINAR_22K'
PGGoldJewellery22KModel._meta.table_name = 'PUBLIC_GOLD_GOLD_JEWELLERY_22K'
PGSilverBullionModel._meta.table_name = 'PUBLIC_GOLD_SILVER_BULLION'
PGSilverWaferDirhamModel._meta.table_name = 'PUBLIC_GOLD_SILVER_WAFER_DIRHAM'
# ------------------------------------------------------------------------------
# UOB
# ------------------------------------------------------------------------------


class UOBGoldBullionModel(ProductGroupModel):
    weight = TextField()
    gold_type = TextField()
    wm_bank_selling_rm = TextField()
    bank_buying = TextField()
    em_bank_selling_rm = TextField()


UOBGoldBullionModel._meta.table_name = 'UOB_GOLD_BULLION'

db.connect()
db.create_tables([
    MaybankGoldBullionModel,
    MaybankGoldInvestmentAccountModel,
    MaybankSilverInvestmentAccountModel,
    # -------------------------------
    PGGoldBar24KModel,
    PGGoldGoldWaferDinar24KModel,
    PGGoldSmallBarWafer24KModel,
    PGClassicBungamasTaiFook24KModel,
    PGFlexibar24KModel,
    PGGoldGoldWaferDinar22KModel,
    PGGoldJewellery22KModel,
    PGSilverBullionModel,
    PGSilverWaferDirhamModel,
    # -------------------------------
    UOBGoldBullionModel
])
