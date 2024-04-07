from functools import wraps
from flask import Blueprint, session, jsonify, request
from database import engine
from sqlalchemy import text
from strings import *

auth = Blueprint("auth", __name__)


def logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get("logged_in"):
            return f(*args, **kwargs)
        else:
            return jsonify(UNAUTHORIZED), 401

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
                    error = INVALID_PASSWORD
                    return jsonify(error), 400
                else:
                    session.clear()
                    session["email"] = result[4]
                    response = {"message": LOGIN_SUCESS, "data": dict(rows._mapping)}
                    return jsonify(response), 200
            else:
                return jsonify(BAD_CREDENTIALS), 404
