from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return { 'message': 'Store not found'}, 404

    @jwt_required()
    def post(self, name):

        if StoreModel.find_by_name(name):
            return { 'message': "A store with '{}' already exists!".format(name) }, 400

        new_store = StoreModel(name)

        try:
            new_store.save_to_db()
        except:
            return { 'message': 'An error occurred while creating the store' }, 500

        return new_store.json(), 201

    @jwt_required()
    def delete(self, name):

        store_to_delete = StoreModel.find_by_name(name)

        if store_to_delete:
            store_to_delete.delete_from_db()
            return { 'message': 'Store deleted' }, 200

        return { 'message': 'Store not found' }, 404


class StoreList(Resource):

    def get(self):
        return { 'stores': [store.json() for store in StoreModel.query.all()] }
