from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=True)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)

class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Interger, primary_key=True)
    image_url = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer(5), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP, onupdate=db.func.now())

class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Interger, pimary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Interger, nullable=False)
    placed_at = db.Column(db.TIMESTAMP, server_default=db.func.now())


