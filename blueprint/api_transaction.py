from flask import Blueprint, request, jsonify, abort
from config.url import SERVER_PREFIX_URL
from config.response_headers import HEADERS
from database.dao_transaction import Transaction, TransactionConditions
from service.api_auth import token_required
from service.transaction import TransactionService


bp_transaction_api = Blueprint('bp_transaction_api', __name__, url_prefix=f'{SERVER_PREFIX_URL}/api')

# The top x users by total transaction amount of masks within a date range.
# The total amount of masks and dollar value of transactions within a date range.
# Process a user purchases a mask from a pharmacy, and handle all relevant data changes in an atomic transaction.

@bp_transaction_api.route('/v1/transactions/summary', methods=['GET'])
@token_required
def get_transaction_summary():
    if request.method != 'GET':
        abort(405)
    
    query_conditions = TransactionConditions(
        start_date=request.args.get('start_date'),
        end_date=request.args.get('end_date'),
        top_x_users=request.args.get('top_x_users')
    )

    try:
        resp = {
            "is_success": True,
            "message": "OK",
            "data": TransactionService().find_summary(query_conditions)
        }
        return jsonify(resp), 200, HEADERS
    except Exception as e:
        resp = {
            "is_success": False,
            "message": str(e),
            "data": []
        }
        return jsonify(resp), 400, HEADERS

@bp_transaction_api.route('/v1/transactions', methods=['POST'])
@token_required
def get_transaction_summary():
    if request.method != 'POST':
        abort(405)

    transaction_info = Transaction(
        pharmacy_id=request.json.get('pharmacy_id'),
        mask_id=request.json.get('mask_id'),
        user_id=request.json.get('user_id'),
        transaction_amount=request.json.get('transaction_amount'),
        transaction_date=request.json.get('transaction_date')
    )
    
    try:
        TransactionService().do_transaction(transaction_info)
        resp = {
            "is_success": True,
            "message": "OK"
        }
        return jsonify(resp), 200, HEADERS
    except Exception as e:
        resp = {
            "is_success": False,
            "message": str(e)
        }
        return jsonify(resp), 400, HEADERS