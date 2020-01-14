from flask import Flask, jsonify
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

#show a specific item and lets you update and delete a specific item
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")
    parser.add_argument('store_id', type=int, required=True, help="Every item needs a store id")

    @jwt_required()
    def get(self, id):
        item = ItemModel.find_by_item_id(id)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404
    
    @jwt_required()
    def delete(self, id):
        item = ItemModel.find_by_item_id(id)
        if item:
            item.delete()
        return {'message': 'Item Deleted'}, 201

    @jwt_required()
    def put(self, id):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_item_id(id)
        
        if item is None:
            item = ItemModel(data['name'], data['price'], data['store_id'])
        else:
            item.name = data['name']
            item.price = data['price']
            
        item.save()
        return item.json(), 201


# show a list of all items and lets you add a new item
class ItemList(Resource):

    def get(self):
        return {"items": ItemModel.find_all_items() }, 200

    @jwt_required()
    def post(self):
        data = Item.parser.parse_args()

        if ItemModel.find_by_item_name(data['name']):
            return {"message": "Item with name '{}' already exists".format(data['name'])}, 400

        item = ItemModel(data['name'], data['price'], data['store_id'])
        item.save()
        return item.json(), 201

    
