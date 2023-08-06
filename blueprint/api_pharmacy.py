import datetime
from flask import Blueprint, request, jsonify, abort
from config.url import SERVER_PREFIX_URL
from config.response_headers import HEADERS
from database.dao_pharmacy import PharmacyConditions
from service.api_auth import token_required
from service.pharmacy import PharmacyService


bp_pharmacy_api = Blueprint('bp_pharmacy_api', __name__, url_prefix=f'{SERVER_PREFIX_URL}/api')

# Search for pharmacies by name, ranked by relevance to the search term.
# List all pharmacies open at a specific time and on a day of the week if requested.
# List all pharmacies with more or less than x mask products within a price range.

@bp_pharmacy_api.route('/v1/pharmacies/names', methods=['GET'])
@token_required
def search_by_business_hour():
    if request.method != 'GET':
        abort(405)
        
    query_conditions = PharmacyConditions(
        search_keyword=request.args.get('search_keyword'),
    )

    try:
        resp = {
            "is_success": True,
            "message": "OK",
            "data": PharmacyService.find_by_name(query_conditions)
        }
        return jsonify(resp), 200, HEADERS
    except Exception as e:
        resp = {
            "is_success": False,
            "message": str(e),
            "data": []
        }
        return jsonify(resp), 400, HEADERS

@bp_pharmacy_api.route('/v1/pharmacies/business_hour', methods=['GET'])
@token_required
def search_by_business_hour():
    if request.method != 'GET':
        abort(405)
        
    query_conditions = PharmacyConditions(
        business_hour=request.args.get('business_hour'),
        day_of_week=request.args.get('day_of_week')
    )

    try:        
        resp = {
            "is_success": True,
            "message": "OK",
            "data": PharmacyService.find_pharmacy_business_hour(query_conditions)
        }
        return jsonify(resp), 200, HEADERS
    except Exception as e:
        resp = {
            "is_success": False,
            "message": str(e),
            "data": []
        }
        return jsonify(resp), 400, HEADERS

@bp_pharmacy_api.route('/v1/pharmacies/mask_price', methods=['GET'])
@token_required
def search_by_products():
    if request.method != 'GET':
        abort(405)
    
    query_conditions = PharmacyConditions(
        min_price=request.args.get('min_price'),
        max_price=request.args.get('max_price')
    )

    try:
        resp = {
            "is_success": True,
            "message": "OK",
            "data": PharmacyService.find_pharmacy_products(query_conditions)
        }
        return jsonify(resp), 200, HEADERS
    except Exception as e:
        resp = {
            "is_success": False,
            "message": str(e),
            "data": []
        }
        return jsonify(resp), 400, HEADERS

