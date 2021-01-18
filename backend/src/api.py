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


NEWDB = os.environ.get('NEWDB')
if NEWDB and NEWDB.lower() == 'true':
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
def retrieve_drinks_detail(payload):
    drinks = Drink.query.all()

    return jsonify({
        'success': True,
        'drinks': [d.long() for d in drinks]
    }), 200


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(payload):
    body = request.get_json()
    if not body:
        abort(400)

    d = Drink(
        title = body.get('title', ''),
        recipe = json.dumps(body.get('recipe', {}))
    )

    try:
        d.insert()
    except:
        abort(422)

    return jsonify({
        'success': True,
        'drinks': [d.long()]
    }), 200


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    body = request.get_json()
    if not body:
        abort(400)

    d = Drink.query.get(drink_id)
    if not d:
        abort(404)

    d.title = body.get('title', '')
    d.recipe = json.dumps(body.get('recipe', {}))

    try:
        d.update()
    except:
        abort(422)

    return jsonify({
        'success': True,
        'drinks': [d.long()]
    }), 200


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    d = Drink.query.get(drink_id)
    if not d:
        abort(404)
    did = d.id

    try:
        d.delete()
    except:
        abort(422)

    return jsonify({
        'success': True,
        'delete': did
    }), 200


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
