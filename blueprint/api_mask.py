from flask import Blueprint, request, jsonify, abort
from config.url import SERVER_PREFIX_URL
from config.response_headers import HEADERS
from database.dao_pharmacy import PharmacyConditions
from database.dao_mask import MaskConditions
from service.api_auth import token_required
from service.mask import MaskService


bp_mask_api = Blueprint('bp_mask_api', __name__, url_prefix=f'{SERVER_PREFIX_URL}/api')


# Search for masks by name, ranked by relevance to the search term.
# List all masks sold by a given pharmacy, sorted by mask name or price.

@bp_mask_api.route('/v1/masks', methods=['GET'])
@token_required
def search_mask():
    if request.method != 'GET':
        abort(405)
    
    query_conditions = MaskConditions(
        search_keyword=request.args.get('search_keyword')
    )

    resp = {
        "is_success": True,
        "message": "OK",
        "data": MaskService.find_by_name(query_conditions)
    }
    return jsonify(resp), 200, HEADERS

@bp_mask_api.route('/v1/pharmacies/<pharmacy_id>/masks', methods=['GET'])
@token_required
def search_by_products(pharmacy_id):
    if request.method != 'GET':
        abort(405)
    
    query_conditions = PharmacyConditions(
        pharmacy_id=pharmacy_id
    )

    try:
        resp = {
            "is_success": True,
            "message": "OK",
            "data": MaskService.find_by_pharmacy(query_conditions)
        }
        return jsonify(resp), 200, HEADERS
    except Exception as e:
        resp = {
            "is_success": False,
            "message": str(e),
            "data": []
        }
        return jsonify(resp), 400, HEADERS