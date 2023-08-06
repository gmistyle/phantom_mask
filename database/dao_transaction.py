import datetime
from sqlalchemy import select, desc, and_, or_, text, func
from dataclasses import dataclass
from engine import ENGINE
from tables import DB_users, DB_transaction_history


# The top x users by total transaction amount of masks within a date range.
# The total amount of masks and dollar value of transactions within a date range.

@dataclass
class Transaction:
    pharmacy_id: int = None
    mask_id: int = None
    user_id: int = None
    transaction_amount: int = None
    transaction_date: datetime.datetime = func.now()
    created_datetime: datetime.datetime = func.now()
    is_deleted: bool = False

@dataclass
class TransactionConditions:
    transaction_id: int = None
    transaction_start_datetime: datetime.datetime = None
    transaction_end_datetime: datetime.datetime = None
    top_x_users: int = 10

class TransactionConditionProcessor:
    @staticmethod
    def get_where_clause(condition: TransactionConditions, satisfy_all_conditions=False):
        filters = list()

        # id
        if condition.transaction_id:
            filters.append(DB_transaction_history.c.id == condition.transaction_id)

        # business hour
        if condition.business_hour:
            filters.append(DB_transaction_history.c.transaction_date <= condition.transaction_start_date)
            filters.append(DB_transaction_history.c.transaction_date >= condition.transaction_end_date)

        filters.append(DB_transaction_history.c.is_deleted == False)
        
        if satisfy_all_conditions == True:
            return and_(*filters)
        else:
            return or_(*filters)

class TransactionDao:
    _alias_user_name = "user_name"
    _alias_transaction_amount = "transaction_amount_sum"
    _alias_transaction_quantity = "transaction_quantity"

    def find_transaction_summary_per_user(self, where_clause):
        with ENGINE.connect() as cnx:
            query = cnx.execute(select([
                DB_users.c.name.label(self._alias_user_name),
                func.ifnull(func.sum(DB_transaction_history.c.amount), 0).label(self._alias_transaction_amount_sum),
                func.ifnull(func.count(DB_transaction_history.c.id), 0).label(self._alias_transaction_quantity),
            ]).select_from(
                DB_users.join(DB_transaction_history, DB_transaction_history.c.user_id == DB_users.c.id)
            ).where(where_clause).order_by(
                desc(func.ifnull(func.sum(DB_transaction_history.c.amount), 0).label(self._alias_transaction_amount_sum))
            )).fetchall()

        return query
