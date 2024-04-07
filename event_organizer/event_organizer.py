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
            error = NAME_EMPTY, 404
        elif data["address"] is None:
            error = ADDRESS_EMPTY, 404
        elif data["email"] is None:
            error = EMAIL_EMPTY, 404
        elif data["password"] is None:
            error = PASSWORD_EMPTY, 404
        elif data["status"] is None:
            error = STATUS_EMPTY, 404

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

                return jsonify(REGISTRATION_SUCESS), 201


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
                error = INVALID_PASSWORD
                return jsonify(error), 400
            else:
                session.clear()
                session["email"] = result[4]
                response = {"message": LOGIN_SUCESS, "data": dict(rows._mapping)}
                return jsonify(response), 200
        else:
            return jsonify(BAD_CREDENTIALS), 404


@event_organizer.route("/logout")
def logout():
    session.pop("email", None)
    return jsonify(LOGOUT_SUCESS), 200
