from Models import db, Users
from flask_restful import Resource, reqparse
from flask_bcrypt import generate_password_hash, check_password_hash

class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('first_name', required=True, help='first_name is required')
    parser.add_argument('last_name', required=True, help='last_name is required')
    parser.add_argument('email', required=True, help='email is required')
    parser.add_argument('password', required=True, help='password is required')
    parser.add_argument('phone_number', required=True, help='phone_number is required')

    def post(self):
        data = User.parser.parse_args()
        data['password'] = generate_password_hash(data['password'])
        data['role'] = 'member'

        user = Users(**data)
        email = Users.query.filter_by(email=data['email']).one_or_none()
        if email:
            return {"message": "email already taken"}
        phone_number = Users.query.filter_by(phone_number=data['phone_number'])
        if phone_number:
            return {"message": "phone number already exists"}
        try:
            db.session.add(user)
            db.session.commit()
            return {"message": "account created successfully", "status": "success"}
        except:
            return {"message": "unable to create account", "status": "fail"}