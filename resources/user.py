from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt import jwt_required

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be left blanck!")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blanck!")
    
    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "User with that username already exists"}, 400
        
        print(data)
        user = UserModel(**data)
        user.save()
        return {"message": "User created successfully", 'user': user.json()}, 201

    def get(self):
        return {'users': UserModel.find_all_users()}

class UserList(Resource):
    @jwt_required()
    def get(self):
        return {'users': UserModel.find_all_users()}
    