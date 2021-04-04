import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'username', type=str, required=True, help="Username field cannot be blank"
    )
    parser.add_argument(
        'password', type=str, required=True, help="Password field cannot be blank"
    )

    def post(self):

        data = self.parser.parse_args()

        # Make sure username doesn't already exist
        if UserModel.find_by_username(data['username']):
            return { "messsage": "Username is already taken. Please try again!" }, 400

        new_user = UserModel(**data)
        new_user.save_to_db()

        return { "message": "User created successfully."}, 201
