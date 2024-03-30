from datetime import datetime
from database import engine
from sqlalchemy import text, exc
from flask import Blueprint, request, jsonify
from strings import *


class event_obj:
    def __init__(self, name, date):
        self.name = name
        self.date = date


events = Blueprint("events", __name__)


# Get all events
@events.route("/")
def get_all_events():

    events = []
    error = None

    with engine.connect() as conn:

        query = text("SELECT * FROM event")

        result = conn.execute(query).fetchall()

        if not result:
            error = NO_EVENTS
            return jsonify(error), 404
        else:

            for row in result:
                events.append(dict(row._mapping))
            return jsonify(events), 200


# Get events by id
@events.route("/<id>")
def get_by_id(id):

    with engine.connect() as conn:

        query = text("SELECT * FROM event where id = :id")
        param = dict(id=id)

        result = conn.execute(query, param).fetchone()

        output = (NO_EVENTS, 404 if result is None else dict(result), 200)

        return jsonify(output)


# Create events
@events.route("/create_event", methods=["GET", "POST"])
def create_eevent():

    name = request.form["name"]
    date = request.form["date"]

    error = None

    if request.method == "POST":
        if not name:
            error = EVENT_NAME_EMPTY
            return jsonify(error), 400
        elif not date:
            error = EVENT_DATE_EMPTY
            return jsonify(error), 400

        if error is None:

            with engine.connect() as conn:

                query = text("INSERT INTO event(name,date) VALUES(:name,:date)")
                params = dict(name=name, date=date)

                conn.execute(query, params)

                conn.commit()
                return jsonify(EVENT_SUCESS), 201


# Update Event

# Delete Event
