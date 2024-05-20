from flask import Flask
from flask_restful import Api 
from flask_migrate import Migrate 
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from Models import db
from Resources.users import User, Login

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BUNDLE_ERRORS'] = True

api = Api(app) 
migrations = Migrate(app, db)
db.init_app(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

 

@app.route('/')
def home():
    return "Hello, world!"
api.add_resource(User, '/users', '/users/<int:id>')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
