from flask import Flask
from flask_restful import Api 
from flask_migrate import Migrate  
from Models import db
from Resources.users import User

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BUNDLE_ERRORS'] = True

migrations = Migrate(app, db)
db.init_app(app)

api = Api(app)  

@app.route('/')
def home():
    return "Hello, world!"
api.add_resource(User, '/users', '/users/<int:id>')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
