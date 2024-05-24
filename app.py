from flask import Flask
from flask_restful import Api 
from flask_migrate import Migrate 
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from Models import db
from resources.products import CreateProduct, FindProduct, UpdateProduct, DeleteProduct
from resources.users import User, Login

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BUNDLE_ERRORS'] = True
app.config["JWT_SECRET_KEY"] = "super-secret"

api = Api(app) 
migrations = Migrate(app, db)
db.init_app(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

 

# Add resources to API
api.add_resource(CreateProduct, '/products')
api.add_resource(FindProduct, '/products', '/products/<int:product_id>')
api.add_resource(UpdateProduct, '/products/<int:product_id>')
api.add_resource(DeleteProduct, '/products/<int:product_id>')

@app.route('/')
def home():
    return "Hello, world!"
api.add_resource(User, '/users', '/users/<int:id>')
api.add_resource(Login, '/login', '/login/<int:id>')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
