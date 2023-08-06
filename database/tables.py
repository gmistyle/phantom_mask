from sqlalchemy import Table, Column, Integer, String, DateTime, Time, Float, Boolean, ForeignKey, MetaData
from sqlalchemy.sql.schema import Index
from sqlalchemy.dialects.mysql import TINYINT
from model.metadata import METADATA
from model.engine import ENGINE


METADATA = MetaData()

def create_tables():
    '''
    Create tables in database if not exists
    '''
    METADATA.create_all(ENGINE)
# 藥局
DB_pharmacy = Table('pharmacy', METADATA,
    Column('id', Integer(), primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False),
    Column('cash_balance', Float(), nullable=False),
    Column('created_at', DateTime(), nullable=False),
    Column('updated_at', DateTime(), nullable=True),
    Column('is_deleted', Boolean(), nullable=False)
)
# 面膜
DB_mask = Table('mask', METADATA,
    Column('id', Integer(), primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False),
    Column('quantity_per_pac', Integer(), nullable=False),
    Column('created_at', DateTime(), nullable=False),
    Column('updated_at', DateTime(), nullable=True),
    Column('is_deleted', Boolean(), nullable=False)
)

# 藥局銷售產品列表
DB_product_list = Table('product_list', METADATA,
    Column('id', Integer(), primary_key=True, autoincrement=True),
    Column('mask_id', Integer(), ForeignKey('mask.id'), nullable=False),
    Column('pharmacy_id', Integer(), ForeignKey('pharmacy.id'), nullable=False),
    Column('sales_price', Float(), nullable=False),
    Column('created_at', DateTime(), nullable=False),
    Column('updated_at', DateTime(), nullable=True),
    Column('is_deleted', Boolean(), nullable=False)
)

# 藥局營業時間
DB_pharmacy_business_hours = Table('pharmacy_opening_hours', METADATA,
    Column('id', Integer(), primary_key=True, autoincrement=True),
    Column('pharmacy_id', Integer(), ForeignKey('pharmacy.id'), nullable=False),
    Column('day_of_week', TINYINT(), nullable=False),
    Column('opening_time', Time(), nullable=False),
    Column('closing_time', Time(), nullable=False),
    Column('created_at', DateTime(), nullable=False),
    Column('updated_at', DateTime(), nullable=True),
    Column('is_deleted', Boolean(), nullable=False)
)

# 使用者
DB_users = Table('users', METADATA,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(100), nullable=False),
    Column('cash_balance', Float(), nullable=False),
    Column('created_at', DateTime(), nullable=False),
    Column('updated_at', DateTime(), nullable=True),
    Column('is_deleted', Boolean(), nullable=False)
)

# 使用者購買紀錄
DB_transaction_history = Table('purchase_history', METADATA,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer(), ForeignKey('users.id'), nullable=False),
    Column('mask_id', Integer(), ForeignKey('mask.id'), nullable=False),
    Column('pharmacy_id', Integer(), ForeignKey('pharmacy.id'), nullable=False),
    Column('transaction_amount', Float(), nullable=False),
    Column('transaction_date', DateTime(), nullable=False),
    Column('created_at', DateTime(), nullable=False),
    Column('updated_at', DateTime(), nullable=True),
    Column('is_deleted', Boolean(), nullable=False)
)

# 添加全文索引 (中文無分割字元，無效)
idx_mask_name_fulltext = Index('idx_mask_name_fulltext', DB_mask.c.name, mysql_length=255, mysql_prefix="FULLTEXT")
idx_pharmacy_name_fulltext = Index('idx_pharmacy_name_fulltext', DB_pharmacy.c.name, mysql_length=255, mysql_prefix="FULLTEXT")