from app import create_app, db
from models import Bull, Vet, Order, OrderBull
from faker import Faker
import random
from datetime import datetime

app = create_app()
fake = Faker()

with app.app_context():
    db.drop_all()
    db.create_all()

    # clear & seed data
    db.session.query(OrderBull).delete()
    db.session.query(Order).delete()
    db.session.query(Bull).delete()
    db.session.query(Vet).delete()

    bulls = []
    for _ in range(5):
        bull = Bull(
            name=fake.first_name(),
            breed=fake.word(),
            description=fake.text(max_nb_chars=200),
            price=random.randint(1000, 5000),
            semen_quantity=random.randint(10, 50),
            image_url=fake.image_url()
        )
        bulls.append(bull)
        db.session.add(bull)

    vets = []
    for _ in range(3):
        vet = Vet(
            name=fake.name(),
            phone=fake.phone_number(),
            email=fake.email(),
            location=fake.city()
        )
        vets.append(vet)
        db.session.add(vet)

    db.session.commit()

    # create orders
    for _ in range(3):
        order = Order(
            customer_name=fake.name(),
            customer_phone=fake.phone_number(),
            order_date=datetime.now(),
            status="pending",
            vet_id=random.choice(vets).id
        )
        db.session.add(order)
        db.session.commit()  # commit order first to get its id

        order_bull = OrderBull(
            order_id=order.id,
            bull_id=random.choice(bulls).id,
            quantity=1,
            price_at_order=random.choice(bulls).price
        )
        db.session.add(order_bull)

    db.session.commit()

    print("✅ Database seeded successfully!")
