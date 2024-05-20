from Models import db, Users
from flask_restful import Resource, reqparse, fields
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

    def post(self):
        data = User.parser.parse_args()
        data['password'] = generate_password_hash(data['password'])
        data['role'] = 'client'

        user = Users(**data)
        email = Users.query.filter_by(email=data['email']).first()

        if email:
            return {"message": "Email already taken", "status": "fail"}, 400

        phone = Users.query.filter_by(phone = data['phone']).one_or_none()

        if phone:
            return {"message": "Phone number already exists", "status": "fail"}, 400
        try:
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)
            return {"message": "account created successfully", "status": "success"}
        except:
            return {"message": "unable to create account", "status": "fail"}
        

class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True, help= 'email is required')
    parser.add_argument('password', required=True, help='password is required')

    def post(self):
        data = Login.parser.add_args()
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
                        "user": user_json,
                        }, 200
            else:
                return {"message": "invalid email/password", "status": "fail"}
        else:
            return {"message": "invalid email/password", "status": "fail"}

class RefreshAccess(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()

        access_token = create_access_token(identity=identity)

        return jsonify(access_token = access_token)