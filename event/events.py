from database import engine
from sqlalchemy import text
from flask import Blueprint, request, jsonify
from strings import *
#from auth.auth import logged_in
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
            error = EVENT_NAME_EMPTY
            response = jsonify(EVENT_NAME_EMPTY)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 400
        elif not data["date"]:
            error = EVENT_DATE_EMPTY
            response = jsonify(EVENT_DATE_EMPTY)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 400

        with engine.connect() as conn:

            query = text(
                "INSERT INTO event(name,date,venue,time,short_description,datetime_created) VALUES(:name,:date,:venue,:time,:short_description,now())"
            )
            params = dict(
                name=data["name"],
                date=data["date"],
                venue=data["venue"],
                time=data["time"],
                short_description=data["short_description"],
            )

            conn.execute(query, params)

            conn.commit()
            response = jsonify(EVENT_SUCESS)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 201


# Update Event

# Delete Event
