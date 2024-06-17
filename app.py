from flask import Flask, jsonify, url_for
from flask_restful import Api
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from Models import db
from resources.products import CreateProduct, FindProduct, UpdateProduct, DeleteProduct
from resources.users import User, Login, confirm_email
from flask_mail import Mail, Message
from resources.orders import OrderResource
from flask_cors import CORS
from itsdangerous import URLSafeSerializer

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BUNDLE_ERRORS'] = True
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'kajmillempire@gmail.com'
app.config['MAIL_PASSWORD'] = 'hdrs bjry dmzv unkn'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
api = Api(app)
migrations = Migrate(app, db)
db.init_app(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
serializer = URLSafeSerializer(app.config["JWT_SECRET_KEY"])

# Add resources to API
api.add_resource(CreateProduct, '/products')
api.add_resource(FindProduct, '/products', '/products/<int:product_id>')
api.add_resource(UpdateProduct, '/products/<int:product_id>')
api.add_resource(DeleteProduct, '/products/<int:product_id>')
api.add_resource(User, '/users', '/users/<int:id>')
api.add_resource(Login, '/login', '/login/<int:id>')
api.add_resource(OrderResource, '/orders', '/orders/<int:order_id>')

@app.route('/')
def home():
    return "Hello, world!"

@app.route('/confirm_email/<token>', methods=['GET'])
def confirm_email_route(token):
    return confirm_email(token)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
