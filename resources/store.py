from flask_restful import Resource, reqparse
from models.store import StoreModel

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="This field cannot be left blank!")
 
    def get(self, id):
        store = StoreModel.find_by_store_id(id)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def delete(self, id):
        store = StoreModel.find_by_store_id(id)
        if store:
            store.delete()
        return {'message': 'Store deleted'}

class StoreList(Resource):
    def get(self):
        return {'stores': StoreModel.find_all_stores() }
        pass

    def post(self):
        data = Store.parser.parse_args()
        if StoreModel.find_by_store_name(data['name']):
            return {'message':'A Store with name {} already exists'.format(data['name'])}, 400
        store = StoreModel(data['name'])
        store.save()
        return store.json()
