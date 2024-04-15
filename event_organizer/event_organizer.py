from functools import wraps
from flask import Blueprint, request, jsonify, session
from database import engine
from sqlalchemy import text
from strings import *

event_organizer = Blueprint("event_organizer", __name__, template_folder="templates")


@event_organizer.route("/<event_id>/register", methods=["GET", "POST"])
def register(event_id):
    data = request.form()
    error = None

    if request.method == "POST":
        if data["name"] is None:
            response = jsonify(NAME_EMPTY)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 404
        elif data["address"] is None:
            response = jsonify(ADDRESS_EMPTY)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 404
        elif data["email"] is None:
            response = jsonify(EMAIL_EMPTY)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 404
        elif data["password"] is None:
            response = jsonify(PASSWORD_EMPTY)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        elif data["status"] is None:
            response = jsonify(STATUS_EMPTY)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 404

        if error is None:
            with engine.connect() as conn:

                query = text(
                    "INSERT INTO event_organizer(event_id,name,address,email,password,status) VALUE (:event_id,:name,:address,:email,:password,:status)"
                )
                params = dict(
                    event_id=event_id,
                    name=data["name"],
                    address=data["address"],
                    email=data["email"],
                    password=data["password"],
                    status=data["status"],
                )

                conn.execute(query, params)
                conn.commit()

                response = jsonify(REGISTRATION_SUCESS)
                response.headers.add("Access-Control-Allow-Origin", "*")
                return response


@event_organizer.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        with engine.connect() as conn:

            query = text("SELECT * FROM event_organizer WHERE email = :email")
            params = dict(email=email)

            result = conn.execute(query, params).fetchone()
            rows = result

        if result is not None:
            if password != result[5]:
                response = jsonify(INVALID_PASSWORD)
                response.headers.add("Access-Control-Allow-Origin", "*")
                return response, 400

            else:
                session.clear()
                session["email"] = result[4]
                response = jsonify(LOGIN_SUCESS, {"data": dict(rows._mapping)})
                response.headers.add("Access-Control-Allow-Origin", "*")
                return response, 200

        else:
            response = jsonify(BAD_CREDENTIALS)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 401


@event_organizer.route("/logout")
def logout():
    session.pop("email", None)
    response = jsonify(LOGOUT_SUCESS)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 200


# Update Event

# Delete Event
