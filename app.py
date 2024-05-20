from flask import Flask
from flask_restful import Api 
from flask_migrate import Migrate  
from Models import db
from resources.products import CreateProduct, FindProduct, UpdateProduct, DeleteProduct

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BUNDLE_ERRORS'] = True

migrations = Migrate(app, db)
db.init_app(app)

api = Api(app)  

# Add resources to API
api.add_resource(CreateProduct, '/products')
api.add_resource(FindProduct, '/products', '/products/<int:product_id>')
api.add_resource(UpdateProduct, '/products/<int:product_id>')
api.add_resource(DeleteProduct, '/products/<int:product_id>')

@app.route('/')
def home():
    return "Hello, world!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
