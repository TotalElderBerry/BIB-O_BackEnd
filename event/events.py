# from datetime import dateti
from datetime import datetime, timedelta
from database import engine
from sqlalchemy import text
from flask import Blueprint, request, jsonify
from strings import *

# from auth.auth import logged_in
from flask_cors import CORS

events = Blueprint("events", __name__)
CORS(events)


# Get all events
@events.route("/")
# @logged_in
def get_all_events():

    events = []

    with engine.connect() as conn:

        query = text("SELECT * FROM event")

        result = conn.execute(query).fetchall()

        if not result:
            response = jsonify(NO_EVENTS)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 400
        else:

            for row in result:
                events.append(dict(row._mapping))
                response = jsonify(EVENT_EXISTS, {"data": events})
                response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 200


# Get events by id
@events.route("/<id>", methods={"GET", "POST"})
# @logged_in
def get_by_id(id):

    if request.method == "GET":
        with engine.connect() as conn:

            query = text("SELECT * FROM event where id = :id")
            param = dict(id=id)

            result = conn.execute(query, param).fetchone()

            if result is None:
                response = jsonify(NO_EVENTS)
                response.headers.add("Access-Control-Allow-Origin", "*")
                return jsonify(response), 400
            else:
                response = jsonify(EVENT_RETRIEVED, {"data": dict(result)})
                response.headers.add("Access-Control-Allow-Origin", "*")
                return jsonify(response), 200


# Create events
@events.route("/create_event", methods=["GET", "POST"])
# @logged_in
def create_eevent():

    data = request.form

    if request.method == "POST":
        if not data["name"]:

            response = jsonify(EVENT_NAME_EMPTY)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 400
        elif not data["date"]:
            response = jsonify(EVENT_DATE_EMPTY)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 400

        with engine.connect() as conn:

            query = text(
                "INSERT INTO event(name,date,venue,time_start,time_end,short_description,no_of_participants,datetime_created) VALUES(:name,:date,:venue,:time,:short_description,now())"
            )
            params = dict(
                name=data["name"],
                date=data["date"],
                venue=data["venue"],
                time_start=data["time_start"],
                time_end=data["time_end"],
                short_description=data["short_description"],
                no_of_participants=data["no_of_participants"],
            )

            conn.execute(query, params)

            conn.commit()
            response = jsonify(EVENT_SUCESS)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 201


# Update Event
@events.route("/update_event/<event_id>", methods=["PUT"])
def update_event(event_id):

    data = request.form

    current_date = datetime.now().date
    current_time = datetime.now().time

    event_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
    event_time_start = datetime.strptime(data["time_start"], "%H:%M:%S").time()
    event_time_end = datetime.strptime(data["time_end"], "%H:%M:%S").time()

    combined_current_datetime = datetime.combine(current_date, current_time)
    combined_event_datetime = datetime.combine(event_date, event_time_end)

    if combined_current_datetime > combined_event_datetime:
        data["status"] = "Finished"

    elif (
        current_date == event_date
        and current_time >= event_time_start
        and current_time <= event_time_end
    ):
        data["status"] = "Ongoing"
        

    with engine.connect() as conn:

        query = text(
            "UPDATE event SET name = :name, date = :date, venue = :venue, time_start = :time_start, time_end = :time_end, short_description = :short_description, no_of_participants = :no_of_participants, status = :status WHERE id = :id"
        )

        params = dict(
            id=event_id,
            name=data["name"],
            date=data["date"],
            venue=data["venue"],
            time_start=data["time_start"],
            time_end=data["time_end"],
            short_description=data["short_description"],
            no_of_participants=data["no_of_participants"],
        )
        result = conn.execute(query, params)

        conn.commit()

        if result.rowcount > 0:
            response = jsonify(UPDATE_EVENT)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 200
        else:
            response = jsonify(FAILED_UPDATE)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 400


# Delete Event
@events.route("/delete_event/<event_id>", methods=["DELETE"])
def delete_event(event_id):

    with engine.connect() as conn:

        query = text("DELETE from event WHERE id = :id")
        params = dict(id=event_id)

        result = conn.execute(query, params)

        conn.commit()

        if result.rowcount > 0:
            response = jsonify(DELETED_EVENT)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 200
        else:
            response = jsonify(FAILED_DELETE)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 400
