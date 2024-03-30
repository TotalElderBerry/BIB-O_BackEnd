from flask import Blueprint, session, jsonify, request
from database import engine
from sqlalchemy import text
from strings import *

auth = Blueprint("auth", __name__)


@auth.routes("/login")
def login():
    def login():

        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            error = None

            with engine.connect() as conn:

                query = text("SELECT * FROM event_organizer WHERE email = :email")
                params = dict(email=email)

                result = conn.execute(query, params)
                rows = result.fetchone()

                if email is None:
                    error = INVALID_EMAIL
                    return jsonify(error)
                elif password != rows[5]:
                    error = INVALID_PASSWORD
                    return jsonify(error)
                elif email or password is None:
                    error = EMAIL_PASSWORD_EMPTY
                    return jsonify(error)

                if error is None:
                    session.clear()
                    session["email"] = rows[4]
                    user_session = {"user": session["email"]}
                    return jsonify(user_session, LOGIN_SUCESS)


@event_organizer.route("/logout")
def logout():
    session.pop("email", None)
    return redirect(url_for("login"), message=LOGOUT_SUCESS)
