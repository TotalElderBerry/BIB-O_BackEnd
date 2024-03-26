from datetime import datetime
from database import engine
from sqlalchemy import text, exc
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from strings import (
    NO_EVENTS,
    EVENT_DATE_EMPTY,
    EVENT_NAME_EMPTY,
    EVENT_EXISTS,
    EVENT_SUCESS,
)


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

        if error is None:
            query = text("SELECT * FROM event")

            result = conn.execute(query).fetchall()

            if len(result) is None:

                error = NO_EVENTS

            else:

                for row in result:
                    events.append(dict(row._mapping))
                return events

    flash(error)

    return jsonify(events)


# Get events by id
@events.route("/<id>")
def get_by_id(id):

    with engine.connect() as conn:

        query = text("SELECT * FROM event where id = :id")
        param = dict(id=id)

        result = conn.execute(query, param).fetchone()

        output = error = NO_EVENTS if len(result) == 0 else dict(result._mapping)

        # return render_template("events.vue", events=output, error=error)

        return jsonify(output)


# Create events
@events.route("/create_event", methods=["GET", "POST"])
def create_eevent():

    name = request.form["name"]
    date = request.form["date"]

    error = None

    if request.method == "POST":
        if name is None:
            error = EVENT_NAME_EMPTY
        elif date is None:
            error = EVENT_DATE_EMPTY

        if error is None:

            with engine.connect() as conn:

                try:
                    query = text("INSERT INTO event(name,date) VALUES(:name,:date)")
                    params = dict(name, date)

                    conn.execute(query, params)

                    conn.commit()

                except exc.IntegrityError as e:
                    error = EVENT_EXISTS

                else:
                    redirect(url_for("event"), message=EVENT_SUCESS)

    return render_template("create_event.vue")


# Update Event

# Delete Event
