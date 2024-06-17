from functools import wraps
from Models import db, Users
from flask_mail import Message
from flask import jsonify
from flask_restful import Resource, reqparse, fields, marshal_with
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_bcrypt import generate_password_hash, check_password_hash

# Admin secret key
ADMIN_SECRET = "5445"

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = Users.query.filter_by(id=current_user_id).first()
        if not user or user.role != 'admin':
            return {"message": "Admins only!"}, 403
        return fn(*args, **kwargs)
    return wrapper

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
    parser.add_argument('role', required=False)  

    @marshal_with(response_field)
    def post(self):

        from app import mail

        data = User.parser.parse_args()
        user_password = data['password']
        data['password'] = generate_password_hash(data['password']).decode('utf8')

        if 'role' in data and data['role'] == ADMIN_SECRET: 
            data['role'] = 'admin'
        else:
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

            msg = Message("confirmation email", sender="kajmillempire@gmail.com", recipients=[data["email"]])
            msg.body = f"Dear {data['first_name']},\n\nYour account has been successfully registered. Your password is: {user_password}\n\nPlease click on the following link to confirm your email: http://localhost:3000"
            mail.send(msg)

            return {
                "message": "Account created successfully",
                "status": "success",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user_json
            }, 201
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
            return self.get_all_users()

    @admin_required
    @jwt_required()
    def get_all_users(self):
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
    parser.add_argument('email', required=True, help='email is required')
    parser.add_argument('password', required=True, help='password is required')

    def post(self):
        data = Login.parser.parse_args()
        user = Users.query.filter_by(email=data['email']).first()

        if user:
            if check_password_hash(user.password, data['password']):  # Validate password
                user_json = user.to_json()
                access_token = create_access_token(identity=user_json['id'])
                refresh_token = create_refresh_token(identity=user_json['id'])
                return {
                    "message": "Login successful",
                    "status": "success",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": user_json
                }, 200
            else:
                return {"message": "Invalid email/password", "status": "fail"}, 400
        else:
            return {"message": "Invalid email/password", "status": "fail"}, 400
