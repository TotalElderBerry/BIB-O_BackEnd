from flask_cors import CORS
from database import engine
from sqlalchemy import text, exc
from flask import Blueprint, request, jsonify
from strings import *

# from auth.auth import logged_in


photographer = Blueprint("photographers", __name__)
CORS(photographer)


@photographer.route("/<event_organizer_id>/", methods=["GET"])
# @logged_in
def get_all(event_organizer_id):
    if request.method == "GET":

        photographers = []

        with engine.connect() as conn:

            query = text("SELECT * FROM photograph")

            result = conn.execute(query).fetchall()

            if query is None:
                response = jsonify(NO_PHOTOGRAPHERS)
                response.headers.add("Access-Control-Allow-Origin", "*")
                return response, 400
            else:
                for row in result:
                    photographers.append(dict(row._mapping))
                    response = jsonify(GET_PHOTOGRAPHERS, {"data": photographers})
                    response.headers.add("Access-Control-Allow-Origin", "*")
                    return response, 200


@photographer.route("/<event_organizer_id>/<id>")
# @logged_in
def get_by_id(event_organizer_id, id):

    with engine.connect() as conn:

        query = text("SELECT * FROM photographer WHERE id = :id")
        params = dict(id=id)

        result = conn.execute(query, params).fetchone()

        if query is None:
            response = jsonify(NO_PHOTOGRAPHERS)
            response.headers.add("Acccess-Control-Allow-Origin", "*")
            return response, 400
        else:
            response = jsonify(GET_PHOTOGRAPHERS, {"data": dict(result)})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 200


@photographer.route("<event_organizer_id>/registration", methods=["GET", "POST"])
# @logged_in
def register_photographer(event_organizer_id):

    data = request.form

    if request.method == "POST":
        if data["name"] is None:
            return jsonify(NAME_EMPTY), 404
        elif data["address"] is None:
            return jsonify(ADDRESS_EMPTY), 404
        elif data["email"] is None:
            return jsonify(EMAIL_EMPTY), 404
        elif data["status"] is None:
            return jsonify(STATUS_EMPTY), 404

        with engine.connect() as conn:
            query = text(
                "INSERT INTO photographer(event_organizer_id, name, address, email, status,datetime_created) VALUES(:event_organizer_id, :name, :address, :email, :status, now())"
            )

            params = dict(
                event_organizer_id=event_organizer_id,
                name=data["name"],
                address=data["address"],
                email=data["email"],
                status=data["status"],
            )

            conn.execute(query, params)

            conn.commit()
            response = jsonify(PHOTOGRAPHER_REGISTERED_SUCCESSFULLY)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 201
