from flask_restful import Resource
from flask import request, make_response
from extensions import db
from models import Order, Bull, OrderBull

class Orders(Resource):
    def get(self):
        """Return all orders with nested bulls."""
        orders = Order.query.all()
        return [o.to_dict() for o in orders], 200

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
                return {"error": f"Bull {bull_id} not found"}, 404

            if bull.semen_quantity < quantity:
                return {"error": f"Not enough stock for {bull.name}"}, 400

            # Deduct stock
            bull.semen_quantity -= quantity

            # Create OrderBull link
            order_bull = OrderBull(order=new_order, bull=bull, quantity=quantity, price_at_order=bull.price)
            db.session.add(order_bull)

        db.session.commit()

        # Return the new order with nested bulls
        return new_order.to_dict(), 201
