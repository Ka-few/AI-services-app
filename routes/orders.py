from flask_restful import Resource
from flask import request, make_response
from extensions import db
from models import Order, Bull, OrderBull

class Orders(Resource):
    def get(self):
        orders = Order.query.all()
        return make_response([o.to_dict() for o in orders], 200)

    def post(self):
        data = request.get_json()

        # Create new order
        new_order = Order(
            customer_name=data.get("customer_name"),
            customer_phone=data.get("customer_phone"),
            vet_id=data.get("vet_id")
        )
        db.session.add(new_order)

        # Handle bulls in the order
        bulls_data = data.get("bulls", [])  
        for bull_data in bulls_data:
            bull_id = bull_data.get("bull_id")
            quantity = bull_data.get("quantity", 1)

            bull = Bull.query.get(bull_id)
            if not bull:
                return make_response({"error": f"Bull {bull_id} not found"}, 404)

            if bull.semen_quantity < quantity:
                return make_response({"error": f"Not enough stock for {bull.name}"}, 400)

            # Deduct stock
            bull.semen_quantity -= quantity

            # Create order-bull link
            order_bull = OrderBull(order=new_order, bull=bull, quantity=quantity)
            db.session.add(order_bull)

        db.session.commit()
        return make_response(new_order.to_dict(), 201)


class OrderByID(Resource):
    def get(self, order_id):
        order = Order.query.get(order_id)
        if order:
            return make_response(order.to_dict(), 200)
        return make_response({"error": "Order not found"}, 404)

    def put(self, order_id):
        order = Order.query.get(order_id)
        if not order:
            return make_response({"error": "Order not found"}, 404)

        data = request.get_json()
        order.customer_name = data.get("customer_name", order.customer_name)
        order.customer_phone = data.get("customer_phone", order.customer_phone)
        order.status = data.get("status", order.status)

        db.session.commit()
        return make_response(order.to_dict(), 200)

    def delete(self, order_id):
        order = Order.query.get(order_id)
        if not order:
            return make_response({"error": "Order not found"}, 404)

        # restore semen stock when deleting
        for ob in order.bulls_link:
            ob.bull.semen_quantity += ob.quantity

        db.session.delete(order)
        db.session.commit()
        return make_response({}, 204)
