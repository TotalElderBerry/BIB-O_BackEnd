from flask import Blueprint, request, jsonify, session
from database import engine
from sqlalchemy import text
from strings import *
from functools import wraps

event_organizer = Blueprint("event_organizer", __name__, template_folder="templates")


def logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get("logged_in"):
            return f(*args, **kwargs)
        else:
            return jsonify(UNAUTHORIZED), 401

    return decorated_func


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


class event_organizer_obj:

    def __init__(self, event_id, name, address, email, password, status):
        self.event_id = event_id
        self.name = name
        self.address = address
        self.email = email
        self.password = password
        self.status = status
