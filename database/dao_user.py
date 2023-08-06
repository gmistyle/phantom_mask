from sqlalchemy.sql import update
from database.engine import ENGINE
from database.tables import DB_users


class UserDao:
    def modify_cash_balance(self, user_id: int, transaction_amount: float):
        with ENGINE.connect() as cnx:
            cnx.execute(update(DB_users).values(
                cash_balance=DB_users.c.cash_balance + transaction_amount
            ).where(
                DB_users.c.id == user_id
            ))