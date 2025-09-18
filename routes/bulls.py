from flask_restful import Resource
from flask import request, make_response
from extensions import db
from models import Bull

class Bulls(Resource):
    def get(self):
        bulls = Bull.query.all()
        return [b.to_dict() for b in bulls], 200   # ✅ serializer used

    def post(self):
        data = request.get_json()
        new_bull = Bull(
            name=data.get("name"),
            breed=data.get("breed"),
            age=data.get("age"),
            semen_quantity=data.get("semen_quantity", 0),
            image_url=data.get("image_url")
        )
        db.session.add(new_bull)
        db.session.commit()
        return new_bull.to_dict(), 201             # ✅ serializer used


class BullByID(Resource):
    def get(self, bull_id):
        bull = Bull.query.get(bull_id)
        if bull:
            return bull.to_dict(), 200             # ✅ serializer used
        return {"error": "Bull not found"}, 404

    def put(self, bull_id):
        bull = Bull.query.get(bull_id)
        if not bull:
            return {"error": "Bull not found"}, 404

        data = request.get_json()
        bull.name = data.get("name", bull.name)
        bull.breed = data.get("breed", bull.breed)
        bull.age = data.get("age", bull.age)
        bull.semen_quantity = data.get("semen_quantity", bull.semen_quantity)
        bull.image_url = data.get("image_url", bull.image_url)

        db.session.commit()
        return bull.to_dict(), 200                 # ✅ serializer used

    def delete(self, bull_id):
        bull = Bull.query.get(bull_id)
        if not bull:
            return make_response({"error": "Bull not found"}, 404)

        db.session.delete(bull)
        db.session.commit()
        return make_response({}, 204)
