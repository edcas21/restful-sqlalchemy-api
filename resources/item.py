from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

# Every resource has to be a class that inherits from Resource
class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be left blank!')
    parser.add_argument('store_id', type=int, required=True, help='Every item needs a store id!')

    # Regular methods
    def get(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return { 'message': 'Item not found' }, 404

    @jwt_required()
    def post(self, name):

        # Making sure name is unique
        if ItemModel.find_by_name(name):
            # 400 is bad request
            return { 'message': "An item with name '{name}' already exists!".format(name=name) }, 400

        # Accessing the json payload
        req_body = Item.parser.parse_args()

        item = ItemModel(name, req_body['price'], req_body['store_id'])

        try:
            item.save_to_db()
        except:
            return { 'message': 'An error occurred inserting the item' }, 500 # Internal server error

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):

        req_body = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = req_body['price']
            item.store_id = req_body['store_id']
        else:
            item = ItemModel(name, **req_body)

        item.save_to_db()

        return item.json()


class ItemList(Resource):

    def get(self):
        return { 'items': list(map(lambda x: x.json(), ItemModel.query.all())) }
