from flask_cors import CORS
from database import engine
from sqlalchemy import text, exc
from flask import Blueprint, request, jsonify
from strings import *

# from auth.auth import logged_in


photographer = Blueprint("photographers", __name__)
CORS(photographer)


@photographer.route("/", methods=["GET"])
# @logged_in
def get_all():
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


@photographer.route("/<id>")
# @logged_in
def get_by_id(id):

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


@photographer.route("/registration", methods=["GET", "POST"])
# @logged_in
def register_photographer():

    data = request.form

    if request.method == "POST":
        if data["name"] is None:
            return jsonify(NAME_EMPTY), 404
        elif data["address"] is None:
            return jsonify(ADDRESS_EMPTY), 404
        elif data["email"] is None:
            return jsonify(EMAIL_EMPTY), 404

        with engine.connect() as conn:
            query = text(
                "INSERT INTO photographer(name, address, email, password,datetime_created) VALUES(:name, :address, :email, :password, now())"
            )

            params = dict(
                name=data["name"],
                address=data["address"],
                email=data["email"],
                password=data["password"],
            )

            result = conn.execute(query, params)

            conn.commit()

            if result.rowcount > 0:

                response = jsonify(PHOTOGRAPHER_REGISTERED_SUCCESSFULLY)
                response.headers.add("Access-Control-Allow-Origin", "*")
                return response, 201

            else:

                response = jsonify(FAILED_REGISTRATION_PHOTOGRAPHER)
                response.headers.add("Access-Control-Allow-Origin", "*")
                return response, 400


@photographer.route("/update/<id>")
def update_event_organizer(id):

    data = request.form

    with engine.connect() as conn:

        query = text(
            "UPDATE photographer SET name = :name, address = :address, email =:email, password = :password WHERE id = :id"
        )
        params = dict(
            id=id,
            name=data["name"],
            address=data["address"],
            email=data["email"],
            password=data["password"],
        )

        result = conn.execute(query, params)

        conn.commit()

        if result.rowcount > 0:
            response = jsonify(UPDATE_PHOTOGRAPHER_SUCCESS)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 200
        else:

            response = jsonify(UPDATE_PHOTOGRAPHER_UNSUCCESSFUL)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 400
