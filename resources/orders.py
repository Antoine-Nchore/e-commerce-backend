from flask_restful import Resource, reqparse, fields, marshal_with
from flask_jwt_extended import  jwt_required
from Models import db, Orders

class OrderResource(Resource):
   
    parser = reqparse.RequestParser()
    parser.add_argument("product_id", type=int, required=True, help="Product id is required")  
    parser.add_argument("user_id", type=int, required=True, help="User id is required") 
   
    order_fields = {
        "id": fields.Integer,
        "product_id": fields.Integer,  
        "user_id": fields.Integer, 
        "placed_at": fields.String,
        "product": fields.Nested({
            "image_url": fields.String,
            "description": fields.String,
            "quantity": fields.Integer,
            "price": fields.Integer,
            "product_name": fields.String,
        }),
        "user": fields.Nested({
            "first_name": fields.String, 
             "last_name": fields.String, 
        })
    }

    @marshal_with(order_fields)
    def get(self, order_id=None):
        if order_id:
            order = Orders.query.get(order_id)
            if order:
                return order
            else:
                return {"message": "Order not found"}, 404
        else:
            all_orders = Orders.query.all()
            return all_orders
        
    @jwt_required()
    @marshal_with(order_fields)
    def post(self):
        args = OrderResource.parser.parse_args()
        order = Orders(**args) 
        try:
            db.session.add(order)
            db.session.commit()

            return {"message": "Order created successfully", "order": order}, 201
        except:
            return{"message": "Order not placed"}
    

    @jwt_required()
    def delete(self, order_id=None):
        if order_id:
            order = Orders.query.get(order_id)
            if order:
                db.session.delete(order)
                db.session.commit()
                return {"message": "Order deleted successfully"}, 200
            else:
                return {"message": "Order not found"}, 404
        else:
            Orders.query.delete()
            db.session.commit()
            return {"message": "All orders deleted successfully"}, 200