from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import check_password_hash

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
    verified = db.Column(db.Boolean, default=False, nullable=False)

    orders = db.relationship("Orders", backref="user", lazy=True, cascade="all, delete-orphan")

    def check_password(self, plain_password):
        return check_password_hash(self.password, plain_password)

    def to_json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "role": self.role,
            "phone_number": self.phone_number,
            "verified": self.verified
        }

class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    orders = db.relationship("Orders", backref="product", lazy=True, cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

class Orders(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id", ondelete="CASCADE", name='fk_orders_product_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE", name='fk_orders_user_id'), nullable=False)
    placed_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
