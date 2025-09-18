from flask_restful import Resource
from flask import request, make_response
from extensions import db
from models import Vet

class Vets(Resource):
    def get(self):
        vets = Vet.query.all()
        return make_response([v.to_dict() for v in vets], 200)

    def post(self):
        data = request.get_json()
        new_vet = Vet(
            name=data.get("name"),
            location=data.get("location"),
            phone=data.get("phone"),
            email=data.get("email")
        )
        db.session.add(new_vet)
        db.session.commit()
        return make_response(new_vet.to_dict(), 201)

class VetByID(Resource):
    def get(self, vet_id):
        vet = Vet.query.get(vet_id)
        if vet:
            return make_response(vet.to_dict(), 200)
        return make_response({"error": "Vet not found"}, 404)

    def put(self, vet_id):
        vet = Vet.query.get(vet_id)
        if not vet:
            return make_response({"error": "Vet not found"}, 404)

        data = request.get_json()
        vet.name = data.get("name", vet.name)
        vet.location = data.get("location", vet.location)
        vet.phone = data.get("phone", vet.phone)
        vet.email = data.get("email", vet.email)

        db.session.commit()
        return make_response(vet.to_dict(), 200)

    def delete(self, vet_id):
        vet = Vet.query.get(vet_id)
        if not vet:
            return make_response({"error": "Vet not found"}, 404)

        db.session.delete(vet)
        db.session.commit()
        return make_response({}, 204)
