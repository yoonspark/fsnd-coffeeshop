import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth


app = Flask(__name__)
setup_db(app)
CORS(app)


RESTART_DB = False # Should be True for the first run
if RESTART_DB:
    db_drop_and_create_all()


@app.route('/drinks')
def retrieve_drinks():
    drinks = Drink.query.all()

    return jsonify({
        'success': True,
        'drinks': [d.short() for d in drinks]
    }), 200


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def retrieve_drinks_detail():
    drinks = Drink.query.all()

    return jsonify({
        'success': True,
        'drinks': [d.long() for d in drinks]
    }), 200


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink():
    body = request.get_json()
    if body:
        d = Drink()
        d.title = body.get('title', ''),
        d.recipe = json.dumps(body.get('recipe', {}))
    else:
        abort(400)

    try:
        d.insert()
    except:
        abort(422)

    return jsonify({
        'success': True,
        'drinks': [d.long()]
    }), 200


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request",
    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found",
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable entity',
    }), 422


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code
