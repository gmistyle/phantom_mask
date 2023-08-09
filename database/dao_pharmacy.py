import datetime
from sqlalchemy import select, update, desc, and_, or_, text
from dataclasses import dataclass
from engine import ENGINE
from tables import DB_pharmacy, DB_product_list, DB_mask, DB_pharmacy_opening_hours


@dataclass
class PharmacyConditions:
    search_keyword: str = None
    # pharmacy
    pharmacy_id: int = None
    opening_hour: datetime.time = None
    day_of_week: int = None, 'enum from 1 to 7, representing Monday to Sunday'
    # Product
    min_price: int = None
    max_price: int = None

class PharmacyConditionProcessor:
    @staticmethod
    def get_where_clause(condition: PharmacyConditions, satisfy_all_conditions=False):
        filters = list()

        # keyword
        if condition.search_keyword:
            filters.append(text("MATCH (name) AGAINST (:keyword IN NATURAL LANGUAGE MODE)").bindparams(keyword=condition.search_keyword))

        # id
        if condition.pharmacy_id:
            filters.append(DB_pharmacy.c.id == condition.pharmacy_id)

        # business hour
        if condition.opening_hour:
            filters.append(DB_pharmacy_opening_hours.c.open_time <= condition.opening_hour)
            filters.append(DB_pharmacy_opening_hours.c.close_time >= condition.opening_hour)
    
        if condition.day_of_week:
            filters.append(DB_pharmacy_opening_hours.c.day_of_week.in_(condition.day_of_week))

        # product price
        if condition.min_price:
            filters.append(DB_product_list.c.sales_price >= condition.min_price)

        if condition.max_price:
            filters.append(DB_product_list.c.sales_price <= condition.max_price)

        filters.append(DB_pharmacy.c.is_deleted == False)
        
        if satisfy_all_conditions == True:
            return and_(*filters)
        else:
            return or_(*filters)
        
class PharmacyDao:
    _alias_pharmacy_id = "pharmacy_id"
    _alias_pharmacy_name = "pharmacy_name"
    _alias_pharmacy_balance = "pharmacy_balance"
    _alias_Pharmacy_business_day_of_week = "day_of_week"
    _alias_pharmacy_open_time = "open_time"
    _alias_pharmacy_close_time = "close_time"
    _alias_mask_id = "mask_id"
    _alias_mask_name = "mask_name"
    _alias_product_sales_price = "mask_price"

    # pharmacy join opening_hour
    def query_pharmacy_join_opening_hour(self, where_clause):
        with ENGINE.connect() as cnx:
            query = cnx.execute(select([
                DB_pharmacy.c.id.label(self._alias_pharmacy_id),
                DB_pharmacy.c.name.label(self._alias_pharmacy_name),
                DB_pharmacy.c.balance.label(self._alias_pharmacy_balance),
                DB_pharmacy_opening_hours.c.day_of_week.label(self._alias_Pharmacy_business_day_of_week),
                DB_pharmacy_opening_hours.c.open_time.label(self._alias_pharmacy_open_time),
                DB_pharmacy_opening_hours.c.close_time.label(self._alias_pharmacy_close_time)
            ]).select_from(
                DB_pharmacy.join(DB_pharmacy_opening_hours, DB_pharmacy.c.id == DB_pharmacy_opening_hours.c.pharmacy_id)
            ).order_by(
                DB_pharmacy_opening_hours.c.day_of_week
            ).where(where_clause)).fetchall()

        return query

    # pharmacy join product_list join mask
    def query_pharmacy_join_product_list_and_mask(self, where_clause):
        with ENGINE.connect() as cnx:
            query = cnx.execute(select([
                DB_pharmacy.c.id.label(self._alias_pharmacy_id),
                DB_pharmacy.c.name.label(self._alias_pharmacy_name),
                DB_pharmacy.c.cash_balance.label(self._alias_pharmacy_balance),
                DB_mask.c.id.label(self._alias_mask_id),
                DB_mask.c.name.label(self._alias_mask_name),
                DB_product_list.c.sales_price.label(self._alias_product_sales_price)
            ]).select_from(
                DB_pharmacy.join(
                    DB_product_list, DB_product_list.c.pharmacy_id == DB_pharmacy.c.id
                ).join(
                    DB_mask, DB_mask.c.id == DB_product_list.c.mask_id
                )
            ).where(where_clause)).fetchall()

        return query

    def query_by_fulltext(self, where_clause, keyword: str):
        fulltext_search = text("MATCH (name) AGAINST (:keyword IN NATURAL LANGUAGE MODE)").bindparams(keyword=keyword)

        # 執行全文檢索並按照關聯性排序
        with ENGINE.connect() as cnx:
            query = cnx.execute(select([
                DB_pharmacy.c.id.label(self._alias_pharmacy_id),
                DB_pharmacy.c.name.label(self._alias_pharmacy_name),
                DB_pharmacy.c.balance.label(self._alias_pharmacy_balance),
            ]).where(where_clause).order_by(
                desc(fulltext_search)
            )).fetchall()

        return query

    def modify_cash_balance(self, pharmacy_id: int, transaction_amount: float):
        with ENGINE.connect() as cnx:
            cnx.execute(update(DB_pharmacy).values(
                balance = DB_pharmacy.c.balance + transaction_amount
            ).where(
                DB_pharmacy.c.id == pharmacy_id
            ))