from functools import wraps
from flask import Blueprint, session, jsonify, request
from database import engine
from sqlalchemy import text
from strings import *
from flask_cors import CORS

auth = Blueprint("auth", __name__)
CORS(auth)


def logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get("logged_in"):
            return f(*args, **kwargs)
        else:
            response = jsonify(UNAUTHORIZED)
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 401
            return response

    return decorated_func


@auth.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        with engine.connect() as conn:

            query = text("SELECT * FROM admin WHERE username = :uname")
            params = dict(uname=username)

            result = conn.execute(query, params).fetchone()

            if result is not None:

                if password != result[2]:
                    response = jsonify(INVALID_PASSWORD)
                    response.headers.add("Access-Control-Allow-Origin", "*")
                    response.status_code = 404
                    return response
                else:
                    session["logged_in"] = True
                    session["id"] = result[0]
                    response = jsonify(LOGIN_SUCESS)
                    response.headers.add("Access-Control-Allow-Origin", "*")
                    response.status_code = 200
                    return response

            else:
                response = jsonify(BAD_CREDENTIALS)
                response.headers.add("Access-Control-Allow-Origin", "*")
                response.status_code = 400
                return response


@auth.route("/event_organizer/login", methods=["GET", "POST"])
def event_organizer_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        with engine.connect() as conn:

            query = text("SELECT * FROM event_organizer WHERE email = :email")
            params = dict(email=email)

            result = conn.execute(query, params).fetchone()

            if result is not None:
                if password != result[3]:
                    response = jsonify(INVALID_PASSWORD)
                    response.headers.add("Access-Control-Allow-Origin", "*")
                    response.status_code = 404
                    return response
                else:
                    session.clear()
                    session["logged_in"] = True
                    session["email"] = result[2]
                    session["id"] = result[0]
                    response = jsonify(LOGIN_SUCESS)
                    response.headers.add("Access-Control-Allow-Origin", "*")
                    response.status_code = 200
                    return response

            else:
                response = jsonify(BAD_CREDENTIALS)
                response.headers.add("Access-Control-Allow-Origin", "*")
                response.status_code = 400
                return response


@auth.route("/photographer/login", methods=["GET", "POST"])
def photographer_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        with engine.connect() as conn:

            query = text("SELECT * FROM photographer WHERE email = :email")
            params = dict(email=email)

            result = conn.execute(query, params).fetchone()
            rows = result

            if result is not None:
                if password != result[4]:
                    response = jsonify(INVALID_PASSWORD)
                    response.headers.add("Access-Control-Allow-Origin", "*")
                    response.status_code = 404
                    return response
                else:
                    session.clear()
                    session["logged_in"] = True
                    session["email"] = result[3]
                    session["id"] = result[0]
                    response = jsonify(LOGIN_SUCESS, {"data": rows[0]})
                    response.headers.add("Access-Control-Allow-Origin", "*")
                    response.status_code = 200
                    return response

            else:
                response = jsonify(BAD_CREDENTIALS)
                response.headers.add("Access-Control-Allow-Origin", "*")
                response.status_code = 400
                return response


@auth.route("/runner/login", methods=["GET", "POST"])
def runner_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        with engine.connect() as conn:

            query = text("SELECT * FROM runner WHERE email = :email")
            params = dict(email=email)

            result = conn.execute(query, params).fetchone()
            rows = result

            if result is not None:
                if password != result[4]:
                    response = jsonify(INVALID_PASSWORD)
                    response.headers.add("Access-Control-Allow-Origin", "*")
                    response.status_code = 404
                    return response
                else:
                    session.clear()
                    session["logged_in"] = True
                    session["email"] = result[3]
                    session["id"] = result[0]
                    response = jsonify(LOGIN_SUCESS, {"data": rows[0]})
                    response.headers.add("Access-Control-Allow-Origin", "*")
                    response.status_code = 200
                    return response

            else:
                response = jsonify(BAD_CREDENTIALS)
                response.headers.add("Access-Control-Allow-Origin", "*")
                response.status_code = 400
                return response


@auth.route("/logout", methods=["POST"])
def logout():
    session.pop("email", None)
    response = jsonify(LOGOUT_SUCESS)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.status_code = 200
    return response
