from functools import wraps
import random
from flask import (
    Blueprint,
    current_app,
    render_template_string,
    request,
    jsonify,
    session,
)
from database import engine
from sqlalchemy import text
from strings import *
from runner.runners import get_all_runners
from flask_mail import Mail, Message

event_organizer = Blueprint("event_organizer", __name__)

mail = Mail()


# Get events by id
@event_organizer.route("/<id>", methods=["GET", "POST"])
# @logged_in
def get_by_id(id):

    if request.method == "GET":
        with engine.connect() as conn:

            query = text("SELECT * FROM event_organizer where id = :id")
            param = dict(id=id)

            result = conn.execute(query, param).fetchone()

            if result is None:
                response = jsonify(NO_EVENTS)
                response.headers.add("Access-Control-Allow-Origin", "*")
                response.status_code = 400
                return response
            else:
                response = jsonify(EVENT_RETRIEVED, {"data": dict(result._mapping)})
                response.headers.add("Access-Control-Allow-Origin", "*")
                response.status_code = 200
                return response


@event_organizer.route("/register", methods=["GET", "POST"])
def register():
    data = request.form
    error = None

    if request.method == "POST":

        if data["name"] is None:
            response = jsonify(NAME_EMPTY)
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 400
            return response
        elif data["address"] is None:
            response = jsonify(ADDRESS_EMPTY)
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 400
            return response
        elif data["email"] is None:
            response = jsonify(EMAIL_EMPTY)
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 400
            return response
        elif data["password"] is None:
            response = jsonify(PASSWORD_EMPTY)
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 400
            return response

        if error is None:
            with engine.connect() as conn:

                query = text(
                    "INSERT INTO event_organizer(name,email,password,datetime_created) VALUE (:name,:email,:password, now())"
                )
                params = dict(
                    name=data["name"],
                    email=data["email"],
                    password=data["password"],
                )

                result = conn.execute(query, params)
                conn.commit()

                if result.rowcount > 0:
                    response = jsonify(REGISTRATION_SUCCESS)
                    response.headers.add("Access-Control-Allow-Origin", "*")
                    response.status_code = 201
                    return response
                else:
                    response = jsonify(REGISTRATION_UNSUCCESSFUL)
                    response.headers.add("Access-Control-Allow-Origin", "*")
                    response.status_code = 400
                    return response


# get runners under the specific event
@event_organizer.route("/<event_id>/<runner_id>/approve_reg", methods=["GET", "POST"])
def approve_registration(event_id, runner_id):

    if request.method == "POST":

        status_db = get_status_registration(runner_id, event_id)
        flag_check = get_all_runners(event_id)
        if flag_check.status_code == 200:

            data = request.form
            # if status_db == "Pending":

            with engine.connect() as conn:
                update_query = text(
                    "UPDATE event_registration SET status = 'Accepted', bib_no = :bib_no WHERE event_id = :e_id AND runner_id = :r_id"
                )

                category_queue = text(
                    "SELECT category FROM event_registration WHERE runner_id = :r_id AND event_id = :e_id"
                )
                category_params = dict(e_id=event_id, r_id=runner_id)
                category_result = conn.execute(
                    category_queue, category_params
                ).fetchone()

                params = dict(
                    bib_no=generate_bib_number(category_result[0]),
                    r_id=runner_id,
                    e_id=event_id,
                )

                result = conn.execute(update_query, params)
                conn.commit()

                if result.rowcount > 0:
                    return send_mail(runner_id, event_id)
                else:
                    response = jsonify({"success": False, "message": "Error occured"})
                    response.headers.add("Access-Control-Allow-Origin", "*")
                    response.status_code = 400
                    return response
            # else:
            #     response = jsonify(
            #         {"success": False, "message": "status already cancelled / accepted"}
            #     )
            #     response.headers.add("Access-Control-Allow-Origin", "*")
            #     response.status_code = 200
            #     return response


@event_organizer.route("/<event_id>/<runner_id>/reject_reg", methods=["GET", "POST"])
def reject_registration(event_id, runner_id):

    if request.method == "POST":

        status_db = get_status_registration(event_id, runner_id)

        flag_check = get_all_runners(event_id)
        if flag_check.status_code == 200:

            data = request.form

            if status_db == "Pending":

                with engine.connect() as conn:
                    update_query_2 = text(
                        "UPDATE event_registration SET status = :status WHERE event_id = :event_id AND runner_id = :runner_id"
                    )
                    params_2 = dict(
                        event_id=event_id, r_id=runner_id, status=data["status"]
                    )

                    result = conn.execute(update_query_2, params_2)
                    conn.commit()

                    if result.rowcount > 0:
                        update_query_3 = text(
                            "UPDATE event SET current_no_of_participants = current_no_of_participants - 1 WHERE id = :event_id"
                        )
                        params_3 = dict(
                            event_id=event_id,
                        )
                        result = conn.execute(update_query_3, params_3)
                        conn.commit()

                        if result.rowcount > 0:

                            response = jsonify(
                                {"success": False, "message": "Registration rejected"}
                            )
                            response.headers.add("Access-Control-Allow-Origin", "*")
                            response.status_code = 200
                            return response
                        else:
                            response = jsonify(
                                {"success": False, "message": "Error occured"}
                            )
                            response.headers.add("Access-Control-Allow-Origin", "*")
                            response.status_code = 400
                            return response
            else:
                response = jsonify(
                    {"success": False, "message": "status already cancelled / accepted"}
                )
                response.headers.add("Access-Control-Allow-Origin", "*")
                response.status_code = 200
                return response


@event_organizer.route("/update")
def update_event_organizer():

    event_organizer_id = session.get("id")
    data = request.form

    with engine.connect() as conn:

        query = text(
            "UPDATE event_organizer SET name = :name, address = :address, email =:email, password = :password WHERE id = :id"
        )
        params = dict(
            id=event_organizer_id,
            name=data["name"],
            address=data["address"],
            email=data["email"],
            password=data["password"],
        )

        result = conn.execute(query, params)

        conn.commit()

        if result.rowcount > 0:
            response = jsonify(UPDATE_EVENT_ORGANIZER_SUCCESS)
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 200
            return response
        else:

            response = jsonify(UPDATE_EVENT_ORGANIZER_UNSUCCESSFUL)
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 400
            return response


def generate_bib_number(category):
    # Extract the integer part from the category
    category_parts = category.split()  # Split the category string into parts
    for part in category_parts:
        if part.isdigit():
            category_number = int(part)
            break
    else:
        # Handle case where no integer part is found
        raise ValueError("Category does not contain an integer part")

    random_number = random.randint(0, 99999)
    formatted_random_number = f"{random_number:05}"  # Ensure the random number is formatted with leading zeros

    bib_number = f"{category_number}-{formatted_random_number}"
    return bib_number


def get_runner_email(runner_id):
    with engine.connect() as conn:
        query = text("SELECT * FROM runner WHERE id = :runner_id")
        params = dict(runner_id=runner_id)
        result = conn.execute(query, params)
        row = result.fetchone()
        if row:
            return row[0]  # Assuming email is in the first column
        else:
            return None  # or raise an exception or handle as needed


def get_runner_data(runner_id):

    with engine.connect() as conn:
        query = text("SELECT * FROM runner WHERE id = :r_id")
        params = dict(r_id=runner_id)

        result = conn.execute(query, params).fetchone()

        return dict(result._mapping)


def get_status_registration(runner_id, event_id):

    with engine.connect() as conn:

        query = text(
            "SELECT status FROM event_registration WHERE event_id = :e_id AND runner_id = :r_id"
        )

        params = dict(e_id=event_id, r_id=runner_id)

        result = conn.execute(query, params).fetchone()

        return dict(result._mapping)


def get_bib_no(runner_id, event_id):

    with engine.connect() as conn:
        query = text(
            "SELECT * FROM event_registration WHERE runner_id = :r_id AND event_id = :e_id"
        )
        params = dict(r_id=runner_id, e_id=event_id)

        result = conn.execute(query, params).fetchone()

        return dict(result._mapping)


def get_event_id(event_id):

    with engine.connect() as conn:

        query = text("SELECT * FROM event WHERE id = :id")
        params = dict(id=event_id)

        result = conn.execute(query, params).fetchone()

        return dict(result._mapping)


def send_mail(runner_id, event_id):
    data_runner = get_runner_data(runner_id)
    data_reg = get_bib_no(runner_id, event_id)
    data_event = get_event_id(event_id)

    # print(first_name)
    html_content = render_template_string(
        """
  <!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f7f0e3; /* Dirty white */
            margin: 0;
            padding: 0;
        }
        h1 {
            text-align: center;
            color: #ffbf00; /* Light gold */
        }
        hr{
        height: 2px; /* Increase thickness to 10 pixels */
        background-color: #7e57ac;
        }
        .container {
            max-width: 600px;
            margin: 20px auto;
            background-color: #fff; /* Dirty white */
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
            border: 3px solid #7e57ac; /* Purple border */
        }
        .header {
            color: #fff;
            padding: 20px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }
        .logo {
            text-align: center;
        }
        .logo img {
            max-width: 200px;
        }
        .message {
            text-align:center;
            font-family: Arial, sans-serif;
            font-weight: bold;
            font-size: 20px;
            color: #000; /* Black */
            line-height: 1.6;
        }
        .message_1{
          
        }
        .details p {
          font-size: 17px; /* Updated to 17px */
            color: #000;
            line-height: 1.2;
        }
        .footer {
            background-color: #7e57ac; /* Purple */
            padding: 10px 20px;
            border-bottom-left-radius: 7px;
            border-bottom-right-radius: 7px;
            text-align: center;
        }
        .footer p {
            margin: 0;
            color: #fff;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">
                 <img src="https://pbs.twimg.com/media/GNJote-aQAAFIrR?format=png&name=small" alt="Logo">
            </div>
            <hr>
        </div>
        <div class="content">
            <p class = "message">CONFIRMATION RECEIPT</p>
            <div class="details">
            <ul style="list-style-type: none; padding-left: 0;">
                <p><li><b style="color: #7e57ac;">Full Name:</b> <b>{{ first_name }} {{ last_name }}</b></li></p>
                <p><li><b style="color: #7e57ac;">Event Name:</b> <b>{{ event_name }}</b></li></p>
                <p><li><b style="color: #7e57ac;">Event Date:</b> <b>{{ event_date }}</b></li></p>
                <p><li><b style="color: #7e57ac;">Event Time:</b> <b>{{ event_time }}</b></li></p>
                <p><li><b style="color: #7e57ac;">Category:</b> <b>{{ category }}</b></li></p>
                <p><li><b style="color: #7e57ac;">Bib No:</b> <b>{{ bib_no }}</b></li></p>
            </ul>
            </div>
        </div>
        <div class="footer">
            <p><b>&copy; 2024 BIBO. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
    """,
        first_name=data_runner.get("first_name"),
        last_name=data_runner.get("last_name"),
        bib_no=data_reg.get("bib_no"),
        category=data_reg.get("category"),
        event_name=data_event.get("name"),
        event_date=data_event.get("date"),
        event_time=data_event.get("time_start"),
    )
    email = data_runner.get("email")
    msg = Message(
        "Registration Confirmation",
        sender="noreply@gmail.com",
        recipients=["jeremyandyampatin@gmail.com", email],
        html=html_content,
    )
    mail.send(msg)
    response = jsonify({"success": True, "message": "Email sent!"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.status_code = 200
    return response
