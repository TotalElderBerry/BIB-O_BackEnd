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
            return response, 401

    return decorated_func


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        with engine.connect() as conn:

            query = text("SELECT * FROM admin WHERE username = :uname")
            params = dict(uname=username)

            result = conn.execute(query, params).fetchone()
            rows = result

            if result is not None:
                if password != result[2]:
                    response = jsonify(INVALID_PASSWORD)
                    response.headers.add("Access-Control-Allow-Origin", "*")
                    return response, 400
                else:
                    session.clear()
                    session["email"] = result[4]
                    response = jsonify(
                        {"message": LOGIN_SUCESS, "data": dict(rows._mapping)}
                    )
                    response.headers.add("Access-Control-Allow-Origin", "*")
                    return response, 200

            else:
                response = jsonify(BAD_CREDENTIALS)
                response.headers.add("Access-Control-Allow-Origin", "*")
                return response, 400
