from flask import Blueprint, session, jsonify, request
from database import engine
from sqlalchemy import text
from strings import *

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
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


@auth.route("/logout")
def logout():
    session.pop("email", None)
    return jsonify(LOGOUT_SUCESS), 200
