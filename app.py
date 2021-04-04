from flask import Flask, request, jsonify
from flask_restful import Api, reqparse
from flask_jwt import JWT
from datetime import timedelta

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///data.db'
app.secret_key = 'secret-key'
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creates db file and builds tables
@app.before_first_request
def create_tables():
    db.create_all()

# JWT
jwt = JWT(app, authenticate, identity) # /auth
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800) # Setting JWT expiration to 30 min

# Customize successfull authentication response
@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id
    })

# Customize the way jwt handles an authentication error
@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({
        'message': error.description,
        'code': error.status_code
    }), error.status_code

# API
api = Api(app)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':

    db.init_app(app)
    app.run(port=5000, debug=True)
