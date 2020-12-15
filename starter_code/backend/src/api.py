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
@TO_DO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES
'''
@TO_DO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json
    {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks')
def retrieve_drinks():
    # get all drinks as drink.short()
    drinks = Drink.query.order_by(Drink.id).all()
    formated_drinks = [drink.short() for drink in drinks]

    return jsonify({
        'success': True,
        'drinks': formated_drinks
    })

'''
@TO_DO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and
    json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def Drinks_details():
    # get drink details as drink.long()
    drinks = Drink.query.order_by(Drink.id).all()
    drink_detail = [drink.long() for drink in drinks]
    return jsonify({
        'success': True,
        'drinks': drink_detail
    })


'''
@TO_DO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and
    json {"success": True, "drinks": drink}
    where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink():
    data = request.get_json()
    req_title = data.get('title', None)
    req_reciepe = data.get('recipe', None)
    # check if title and recipe is empty abort error
    if req_title is None or req_title == "":
        abort(400)
    if req_reciepe is None or req_reciepe == "":
        abort(400)
    # create new drink
    new_drink = Drink(title=req_title, recipe=json.dumps(req_reciepe))
    new_drink.insert()
    # get all drinks ordered by id
    drinks = Drink.query.order_by(Drink.id).all()
    # format drink in drink.long()
    formatted_Drink = [drink.long() for drink in drinks]
    return jsonify({
        "success": True,
        "drinks": formatted_Drink})
'''
@TO_DO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and
    json {"success": True, "drinks": drink}
    where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def Edit_Drink(id):
    # get required edited drink data
    drink = Drink.query.get(id)
    # if drink not exist in db abort not found
    if not drink:
        abort(404)
    data = request.get_json()
    # if title in requested edited data update new title
    if 'title' in data.keys():
        drink.title = data['title']
    # if recipe in requested edited data update new recipe
    if 'recipe' in data.keys():
        drink.recipe = json.dumps(data['recipe'])
    drink.update()
    # get all drinks ordered by id
    Drinks = Drink.query.order_by(Drink.id).all()
    # format drink in drink.long()
    formatted_drinks = [d.long() for d in Drinks]
    return jsonify({
        "success": True,
        "drinks": formatted_drinks
        })
'''
@TO_DO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and
    json {"success": True, "delete": id}
    where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def remove_drink(id):
    # get requested deleted drink
    drink = Drink.query.get(id)
    # if drink not exist abort 404
    if not drink:
        abort(404)
    drink.delete()
    # return deleted id and success msg
    return jsonify({
        "success": True,
        "delete": id
    })

# Error Handling
'''
Example error handling for unprocessable entity
'''


# error handler
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({"success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


@app.errorhandler(404)
def Not_Found(error):
    return jsonify({"success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404


@app.errorhandler(400)
def Bad_request(error):
    return jsonify({"success": False,
                    "error": 400,
                    "message": "Bad Request"
                    }), 400


@app.errorhandler(405)
def Method_not_allowed(error):
    return jsonify({"success": False,
                    "error": 405,
                    "message": "Method not Allowed"
                    }), 405


@app.errorhandler(500)
def Server_Error(error):
    return jsonify({"success": False,
                    "error": 500,
                    "message": "Internal Server Error"
                    }), 500


# Auth Error handler
@app.errorhandler(AuthError)
def auth_error(exception):
    return jsonify({
        "success": False,
        "error": exception.status_code,
        "message": exception.error['description']
    }), exception.status_code
'''
@TO_DO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TO_DO implement error handler for 404
    error handler should conform to general task above
'''


'''
@TO_DO implement error handler for AuthError
    error handler should conform to general task above
'''
