from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS

from models import db, Bull, Vet, Order, OrderBull

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///bull_catalog.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.json.compact = False

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    api = Api(app)

    # ------------------ Home ------------------
    class Home(Resource):
        def get(self):
            return {"message": "Welcome to Bull Catalog API!"}, 200

    # ------------------ Bulls ------------------
    class BullsResource(Resource):
        def get(self):
            bulls = Bull.query.all()
            return jsonify([b.to_dict() for b in bulls])

        def post(self):
            data = request.get_json()
            new_bull = Bull(
                name=data.get("name"),
                breed=data.get("breed"),
                age=data.get("age"),
                description=data.get("description"),
                image_url=data.get("image_url"),
                semen_quantity=data.get("semen_quantity", 0),
                price=data.get("price", 0.0)
            )
            db.session.add(new_bull)
            db.session.commit()
            return jsonify(new_bull.to_dict()), 201

    class BullByID(Resource):
        def get(self, bull_id):
            bull = Bull.query.get_or_404(bull_id)
            return jsonify(bull.to_dict())

        def put(self, bull_id):
            bull = Bull.query.get_or_404(bull_id)
            data = request.get_json()
            bull.name = data.get("name", bull.name)
            bull.breed = data.get("breed", bull.breed)
            bull.age = data.get("age", bull.age)
            bull.description = data.get("description", bull.description)
            bull.image_url = data.get("image_url", bull.image_url)
            bull.semen_quantity = data.get("semen_quantity", bull.semen_quantity)
            bull.price = data.get("price", bull.price)
            db.session.commit()
            return jsonify(bull.to_dict())

        def delete(self, bull_id):
            bull = Bull.query.get_or_404(bull_id)
            db.session.delete(bull)
            db.session.commit()
            return "", 204

    # ------------------ Vets ------------------
    class VetsResource(Resource):
        def get(self):
            vets = Vet.query.all()
            return jsonify([v.to_dict() for v in vets])

        def post(self):
            data = request.get_json()
            new_vet = Vet(
                name=data.get("name"),
                phone=data.get("phone"),
                email=data.get("email"),
                location=data.get("location")
            )
            db.session.add(new_vet)
            db.session.commit()
            return jsonify(new_vet.to_dict()), 201

    class VetByID(Resource):
        def get(self, vet_id):
            vet = Vet.query.get_or_404(vet_id)
            return jsonify(vet.to_dict())

        def put(self, vet_id):
            vet = Vet.query.get_or_404(vet_id)
            data = request.get_json()
            vet.name = data.get("name", vet.name)
            vet.phone = data.get("phone", vet.phone)
            vet.email = data.get("email", vet.email)
            vet.location = data.get("location", vet.location)
            db.session.commit()
            return jsonify(vet.to_dict())

        def delete(self, vet_id):
            vet = Vet.query.get_or_404(vet_id)
            db.session.delete(vet)
            db.session.commit()
            return "", 204

    # ------------------ Orders ------------------
    class OrdersResource(Resource):
        def get(self):
            orders = Order.query.all()
            return jsonify([o.to_dict() for o in orders])

        def post(self):
            data = request.get_json()
            vet_id = data.get("vet_id")
            vet = Vet.query.get(vet_id) if vet_id else None
            new_order = Order(
                customer_name=data.get("customer_name"),
                customer_phone=data.get("customer_phone"),
                vet=vet
            )
            db.session.add(new_order)
            db.session.commit()
            return jsonify(new_order.to_dict()), 201

    class OrderByID(Resource):
        def get(self, order_id):
            order = Order.query.get_or_404(order_id)
            return jsonify(order.to_dict())

        def put(self, order_id):
            order = Order.query.get_or_404(order_id)
            data = request.get_json()
            order.customer_name = data.get("customer_name", order.customer_name)
            order.customer_phone = data.get("customer_phone", order.customer_phone)
            db.session.commit()
            return jsonify(order.to_dict())

        def delete(self, order_id):
            order = Order.query.get_or_404(order_id)
            db.session.delete(order)
            db.session.commit()
            return "", 204

    # ------------------ Register Routes ------------------
    api.add_resource(Home, "/")
    api.add_resource(BullsResource, "/bulls")
    api.add_resource(BullByID, "/bulls/<int:bull_id>")
    api.add_resource(VetsResource, "/vets")
    api.add_resource(VetByID, "/vets/<int:vet_id>")
    api.add_resource(OrdersResource, "/orders")
    api.add_resource(OrderByID, "/orders/<int:order_id>")

    return app


# ------------------ Run App ------------------
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
