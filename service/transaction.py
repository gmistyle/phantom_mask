from database.dao_user import UserDao
from database.dao_pharmacy import PharmacyDao
from database.dao_transaction import (
    Transaction,
    TransactionConditions,
    TransactionConditionProcessor,
    TransactionDao
)

        
class TransactionService:
    def do_transaction(self, transaction: Transaction):
        if transaction.pharmacy_id == None:
            raise Exception("pharmacy_id is required")
        
        if transaction.mask_id == None:
            raise Exception("mask_id is required")
        
        if transaction.user_id == None:
            raise Exception("user_id is required")

        if Transaction.transaction_amount <= 0:
            raise Exception("transaction_amount must be greater than 0")
        
        if Transaction.transaction_date == None:
            raise Exception("transaction_date is required")
    
        # add transaction history
        TransactionDao().do_transaction(transaction)

        # modify cash balance
        UserDao().modify_cash_balance(transaction.user_id, transaction.transaction_amount)
        PharmacyDao().modify_cash_balance(transaction.pharmacy_id, transaction.transaction_amount)

        return

    def find_summary(self, conditions: TransactionConditions):
        if conditions.transaction_start_date == None:
            raise Exception("transaction_start_date is required")
        
        if conditions.transaction_end_date == None:
            raise Exception("transaction_end_date is required")

        where_clause = TransactionConditionProcessor.get_where_clause(conditions, satisfy_all_conditions=True)
        query_result = TransactionDao().find_transaction_summary_per_user(where_clause)

        rank = 1
        total_transaction_amount = 0
        total_transaction_quantity = 0
        user_result = list()
        for row in query_result:
            total_transaction_amount += getattr(row, TransactionDao._alias_transaction_amount_sum)
            total_transaction_quantity += getattr(row, TransactionDao._alias_transaction_quantity)

            # only return top x users data to frontend
            if len(user_result) >= conditions.top_x_users:
                continue

            user_result.append({
                "rank": rank,
                "user_name": getattr(row, TransactionDao._alias_user_name),
                "transaction_amount_sum": getattr(row, TransactionDao._alias_transaction_amount_sum),
                "transaction_quantity": getattr(row, TransactionDao._alias_transaction_quantity),
            })

            rank += 1

        return {
            "total_transaction_amount": total_transaction_amount,
            "total_transaction_quantity": total_transaction_quantity,
            "top_x_users": user_result
        }
    
