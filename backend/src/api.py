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

'''
@TODO[X] uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
@app.route('/')
def index():
    return jsonify({
        'success': True,
        'message':'hello-coffee'
    }), 200

'''
@TODO[X] implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'], endpoint='get_drinks')
def get_drinks():
    drinks = Drink.query.all()

    try:
        return json.dumps({
            'success':
            True,
            'drinks': [drink.short() for drink in drinks]
        }), 200
    except:
        return json.dumps({
            'success': False,
            'error': "An error occurred"
        }), 500

'''
@TODO[X] implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'], endpoint="drinks_detail")
@requires_auth('get:drinks-detail')
def get_drink_detail(payload):
    drinks = Drink.query.all()

    try:
        return json.dumps({
            'success':
            True,
            'drinks': [drink.long() for drink in drinks]
        }), 200
    except:
        return json.dumps({
            'success': False,
            'error': "An error occurred"
        }), 500

'''
@TODO[X] implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'], endpoint="post_drink")
@requires_auth('post:drinks')
def create_drink(payload):
    data = dict(request.form or request.json or request.data)
    drink = Drink(
                title=data.get('title'),
                recipe=data.get('recipe') if type(data.get('recipe')
                ) == str
                    else json.dumps(data.get('recipe')
                )
            )
    try:
        drink.insert()
        return json.dumps({'success': True, 'drink': drink.long()}), 200
    except:
        return json.dumps({
            'success': False,
            'error': "An error occurred"
        }), 500

'''
@TODO[X] implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'], endpoint="patch_drink")
@requires_auth('patch:drinks')
def update_drink(jwt, id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink is None:
            abort(404)

        data = dict(request.form or request.json or request.data)
        if 'title' in data:
            drink.title = data['title']

        if 'recipe' in data:
            drink.recipe = json.dumps(data['recipe'])

        drink.update()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except:
        return json.dumps({
            'success': False,
            'error': "An error occurred"
        }), 500

'''
@TODO[X] implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()

    if not drink:
        abort(404)

    try:
        drink.delete()
    except BaseException:
        abort(400)

    return jsonify({'success': True, 'delete': id}), 200

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO[X] implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
@TODO[X] implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

'''
@Todo[X] implement internal server error handler
'''
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": 'Internal Server Error'
    }), 500
