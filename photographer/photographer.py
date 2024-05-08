import os
from flask_cors import CORS
from database import engine
from sqlalchemy import text, exc
from flask import Blueprint, current_app, request, jsonify, session
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
                response.status_code = 404
                return response
            else:
                for row in result:
                    photographers.append(dict(row._mapping))
                    response = jsonify(GET_PHOTOGRAPHERS, {"data": photographers})
                    response.headers.add("Access-Control-Allow-Origin", "*")
                    response.status_code = 200
                    return response


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
            response.status_code = 404
            return response
        else:
            response = jsonify(GET_PHOTOGRAPHERS, {"data": dict(result._mapping)})
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 200
            return response


def get_session():
    test = session.get("id")
    print(test)
    return test


@photographer.route("/registration", methods=["GET", "POST"])
# @logged_in
def register_photographer():

    data = request.form

    if request.method == "POST":
        if data["name"] is None:
            response = jsonify(NAME_EMPTY)
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 400
            return response
        elif data["email"] is None:
            response = jsonify(EMAIL_EMPTY)
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 400
            return response

        with engine.connect() as conn:
            query = text(
                "INSERT INTO photographer(name,alias, email, password,datetime_created) VALUES(:name,:alias, :email, :password, now())"
            )

            params = dict(
                name=data["name"],
                alias=data["alias"],
                email=data["email"],
                password=data["password"],
            )

            result = conn.execute(query, params)

            conn.commit()

            if result.rowcount > 0:

                response = jsonify(PHOTOGRAPHER_REGISTERED_SUCCESSFULLY)
                response.headers.add("Access-Control-Allow-Origin", "*")
                response.status_code = 201

                # pk_photographer_id = result.lastrowid

                # if pk_photographer_id is not None:
                #     folder_path = os.path.join(
                #         current_app.static_folder, "gallery", str(pk_photographer_id)
                #     )
                #     os.makedirs(folder_path, exist_ok=True)

                return response

            else:

                response = jsonify(FAILED_REGISTRATION_PHOTOGRAPHER)
                response.headers.add("Access-Control-Allow-Origin", "*")
                response.status_code = 400
                return response


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
            response.status_code = 200
            return response
        else:

            response = jsonify(UPDATE_PHOTOGRAPHER_UNSUCCESSFUL)
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 400
            return response


# upload photos based on the events

# list of photographers under that event
