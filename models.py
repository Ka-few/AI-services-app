from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin


db = SQLAlchemy()


class Bull(db.Model, SerializerMixin):
    __tablename__ = "bulls"
    serialize_rules = ("-order_items.bull",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    breed = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text)

    image_url = db.Column(db.String(255))  # store image path/URL
    semen_quantity = db.Column(db.Integer, default=0)  # available straws
    price = db.Column(db.Float, nullable=False)

    # Relationship with order-bull join
    order_items = db.relationship("OrderBull", back_populates="bull")

    def __repr__(self):
        return f"<Bull {self.name} - {self.breed}, Qty: {self.semen_quantity}>"


class Vet(db.Model, SerializerMixin):
    __tablename__ = "vets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True)
    location = db.Column(db.String(120))

    orders = db.relationship("Order", back_populates="vet")

    def __repr__(self):
        return f"<Vet {self.name}>"


class Order(db.Model, SerializerMixin):
    __tablename__ = "orders"
    serialize_rules = ("-order_items.order", "-vet.orders")

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(20))
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="pending")

    vet_id = db.Column(db.Integer, db.ForeignKey("vets.id"))
    vet = db.relationship("Vet", back_populates="orders")

    # Relationship with order-bull join
    order_items = db.relationship("OrderBull", back_populates="order")

    def __repr__(self):
        return f"<Order {self.id} - {self.customer_name}>"

    # ---------- Business Rules ----------
    def add_bull(self, bull, quantity=1):
        """Add a bull with quantity to the order."""
        if bull.semen_quantity < quantity:
            raise ValueError(f"Not enough stock for {bull.name}")
        bull.semen_quantity -= quantity
        item = OrderBull(order=self, bull=bull, quantity=quantity, price_at_order=bull.price)
        self.order_items.append(item)

    def cancel_order(self):
        """Cancel order and restore semen quantities."""
        if self.status not in ["completed", "cancelled"]:
            for item in self.order_items:
                item.bull.semen_quantity += item.quantity
            self.status = "cancelled"

    def confirm_order(self):
        if self.status == "pending":
            self.status = "confirmed"

    def complete_order(self):
        if self.status == "confirmed":
            self.status = "completed"


class OrderBull(db.Model, SerializerMixin):
    __tablename__ = "order_bulls"
    serialize_rules = ("-order", "-bull")

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), primary_key=True)
    bull_id = db.Column(db.Integer, db.ForeignKey("bulls.id"), primary_key=True)

    quantity = db.Column(db.Integer, nullable=False, default=1)
    price_at_order = db.Column(db.Float, nullable=False)  # lock price

    # Relationships
    order = db.relationship("Order", back_populates="order_items")
    bull = db.relationship("Bull", back_populates="order_items")

    def __repr__(self):
        return f"<OrderBull order={self.order_id}, bull={self.bull_id}, qty={self.quantity}>"
