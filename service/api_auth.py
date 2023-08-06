from functools import wraps
from flask import request, jsonify
from config.access_token import ACCESS_TOKEN
from config.response_headers import HEADERS


def token_required(func):
    '''
    A decorator that would check if token is exist or valid
    '''
    @wraps(func)
    def decorated(*args, **kwargs):        
        try:
            token = request.headers.get('Authorization').split(' ')[1]
        except:
            return jsonify({'message' : 'Token is missing'}), HEADERS

        if not token:
            return jsonify({'message' : 'Token is missing'}), HEADERS

        if token != ACCESS_TOKEN:
            return jsonify({'message' : 'Token is invalid'}), HEADERS

        return func(*args, **kwargs)
    return decorated