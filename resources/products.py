from flask_restful import fields, Resource, reqparse, marshal_with
from Models import db, Products
from datetime import datetime

product_fields = {
    "id": fields.Integer,
    "image_url": fields.String,
    "quantity": fields.Integer,
    "description": fields.String,
    "product_name": fields.String,
    "category": fields.String,
    "rating": fields.Integer,
    "created_at": fields.DateTime,
    "updated_at": fields.DateTime
}

response_field = {
    "message": fields.String,
    "status": fields.String,
    "product": fields.Nested(product_fields)
}

class CreateProduct(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('product_name', required=True, help='product_name is required')
    parser.add_argument('quantity', type=int, required=True, help='quantity is required')
    parser.add_argument('description', required=True, help='Description is required')
    parser.add_argument('image_url', required=True, help='image_url is required')
    parser.add_argument('category', required=True, help='category is required')
    parser.add_argument('rating', type=int, required=True, help='rating is required')

    @marshal_with(response_field)
    def post(self):
        data = CreateProduct.parser.parse_args()

        product = Products(**data)

        db.session.add(product)
        db.session.commit()

        return {"message": "Created Product successfully", "status": "success", "product": product}, 201

class FindProduct(Resource):
    
    def get(self, product_id=None):
        if product_id:
            product = Products.query.get(product_id)
            if product:
                product_data = {
                    "id": product.id,
                    "product_name": product.product_name,
                    "image_url": product.image_url,
                    "category": product.category,
                    "description": product.description,
                    "quantity": product.quantity,
                    "rating": product.rating,
                    "created_at": product.created_at.isoformat() if product.created_at else None,
                    "updated_at": product.updated_at.isoformat() if product.created_at else None,
                }
                return product_data, 200
            else:
                return {"message": "Product not Found"}, 400
        else:
            all_products = Products.query.all()
            products_data = [{
                "id": product.id,
                "product_name": product.product_name,
                "image_url": product.image_url,
                "category": product.category,
                "description": product.description,
                "quantity": product.quantity,
                "rating": product.rating,
                "created_at": product.created_at.isoformat() if product.created_at else None,
                "updated_at": product.updated_at.isoformat() if product.created_at else None,
            } for product in all_products]
            return products_data, 200

class UpdateProduct(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('product_name')
    parser.add_argument('image_url')
    parser.add_argument('quantity', type=int)
    parser.add_argument('rating', type=int)
    parser.add_argument('description')

    @marshal_with(response_field)
    def put(self, product_id):
        data = UpdateProduct.parser.parse_args()
        product = Products.query.get(product_id)
        if product:
            for key, value in data.items():
                if value is not None:
                    setattr(product, key, value)
            product.updated_at = datetime.utcnow()
            db.session.commit()
            return {"message": "Product updated successfully", "status": "success", "product": product}, 200
        else:
            return {"message": "Product not found", "status": "fail"}, 404

class DeleteProduct(Resource):
    def delete(self, product_id):
        product = Products.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return {"message": "Product deleted successfully", "status": "success"}, 200
        else:
            return {"message": "Product not found", "status": "fail"}, 404
