from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister, UserList
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
app.secret_key = "4ad60f75-edd5-4871-96de-b2b8baa40cf2"
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/items/<int:id>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(UserList, '/users')
api.add_resource(Store, '/stores/<int:id>')
api.add_resource(StoreList, '/stores')

@app.errorhandler(404)
def page_not_found(e):
    return {"message": "page not found"}, 404


if __name__ == '__main__':
    from database import db
    db.init_app(app)
    app.run(port=5000, debug=True)