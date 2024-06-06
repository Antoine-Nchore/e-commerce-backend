from Models import db, Users
from flask import jsonify
from flask_restful import Resource, reqparse, fields, marshal_with
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_bcrypt import generate_password_hash

user_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'role': fields.String,
    'phone_number': fields.String
}

response_field = {
    "message": fields.String,
    "status": fields.String,
    "user": fields.Nested(user_fields)
}

class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('first_name', required=True, help='first_name is required')
    parser.add_argument('last_name', required=True, help='last_name is required')
    parser.add_argument('email', required=True, help='email is required')
    parser.add_argument('password', required=True, help='password is required')
    parser.add_argument('phone_number', required=True, help='phone_number is required')

    @marshal_with(response_field)
    def post(self):
        data = User.parser.parse_args()
        data['password'] = generate_password_hash(data['password']).decode('utf8')
        data['role'] = 'client'

        email = Users.query.filter_by(email=data['email']).one_or_none()
        if email:
            return {"message": "Email already taken", "status": "fail"}, 400

        phone_number = Users.query.filter_by(phone_number=data['phone_number']).one_or_none()
        if phone_number:
            return {"message": "Phone number already exists", "status": "fail"}, 400

        try:
            user = Users(**data)
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)

            user_json = user.to_json()
            access_token = create_access_token(identity=user_json['id'])
            refresh_token = create_refresh_token(identity=user_json['id'])

            return {"message": "Account created successfully",
                    "status": "success",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": user_json }, 201
        except Exception as e:
            return {"message": "Unable to create account", "status": "fail", "error": str(e)}, 400

    @jwt_required()
    def get(self, id=None):
        if id:
            user = Users.query.get(id)
            if user:
                user_data = {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "role": user.role,
                    "phone_number": user.phone_number,
                }
                return {"message": "User found", "status": "success", "user": user_data}, 200
            else:
                return {"message": "User not found", "status": "fail"}, 404
        else:
            users = Users.query.all()
            users_data = [{
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "role": user.role,
                    "phone_number": user.phone_number,
            } for user in users]
            return {"message": "Users retrieved", "status": "success", "users": users_data}, 200

class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True, help= 'email is required')
    parser.add_argument('password', required=True, help='password is required')

    def post(self):
        data = Login.parser.parse_args()
        user = Users.query.filter_by(email=data['email']).first()

        if user:
            is_password_correct = user.check_password(data['password'])
            if is_password_correct:
                user_json = user.to_json()
                access_token = create_access_token(identity=user_json['id'])
                refresh_token = create_refresh_token(identity=user_json['id'])
                return {"message": "Login successful",
                        "status": "success",
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "user": user_json}, 200
            else:
                return {"message": "Invalid email/password", "status": "fail"}, 400
        else:
            return {"message": "Invalid email/password", "status": "fail"}, 400
