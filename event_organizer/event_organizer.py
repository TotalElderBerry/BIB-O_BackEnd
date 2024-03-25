from flask import Blueprint, flash, redirect, url_for, render_template, request, session
from database import engine
from sqlalchemy import text, exc
from strings import (
    EMAIL_EMPTY,
    PASSWORD_EMPTY,
    NAME_EMPTY,
    ADDRESS_EMPTY,
    STATUS_EMPTY,
    EMAIL_PASSWORD_EMPTY,
    INVALID_EMAIL,
    INVALID_PASSWORD,
    EMAIL_EXISTS,
    LOGIN_SUCESS,
    LOGOUT_SUCESS,
    REGISTRATION_SUCESS,
)


event_organizer = Blueprint("event_organizer", __name__, template_folder="templates")


@event_organizer.route("/")
def home():
    return "test"


@event_organizer.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        error = None

        with engine.connect() as conn:

            query = text("SELECT * FROM event_organizer WHERE email = :email")
            params = dict(email)

            result = conn.execute(query, params).fetchone()

            if email is None:
                error = INVALID_EMAIL
            elif password != result[5]:
                error = INVALID_PASSWORD
            elif email or password is None:
                error = EMAIL_PASSWORD_EMPTY

            if error is not None:
                session.clear()
                session["email"] = result[4]
                return redirect(url_for("home"), message=LOGIN_SUCESS)

        flash(error)

    return render_template("login.vue")


@event_organizer.route("/<event_id>/register", methods=["GET", "POST"])
def register(event_id):
    data = request.form()
    error = None

    if request.method == "POST":
        if data["name"] is None:
            error = NAME_EMPTY
        elif data["address"] is None:
            error = ADDRESS_EMPTY
        elif data["email"] is None:
            error = EMAIL_EMPTY
        elif data["password"] is None:
            error = PASSWORD_EMPTY
        elif data["status"] is None:
            error = STATUS_EMPTY

        if error is None:
            with engine.connect() as conn:

                try:
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

                except exc.IntegrityError as e:
                    error = EMAIL_EXISTS
                else:
                    return redirect(url_for("login"), message=REGISTRATION_SUCESS)

        flash(error)

    return render_template("registration.vue")


@event_organizer.route("/logout")
def logout():
    session.pop("email", None)
    return redirect(url_for("login"), message=LOGOUT_SUCESS)


class event_organizer_obj:

    def __init__(self, event_id, name, address, email, password, status):
        self.event_id = event_id
        self.name = name
        self.address = address
        self.email = email
        self.password = password
        self.status = status
