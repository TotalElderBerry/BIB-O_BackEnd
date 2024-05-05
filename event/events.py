import os
from datetime import datetime
from auth.auth import logged_in
from database import engine
from sqlalchemy import text
from flask import Blueprint, request, jsonify, current_app, session
from strings import *
from slugify import slugify

# from auth.auth import logged_in
from flask_cors import CORS

events = Blueprint("events", __name__)
CORS(events)


# Get all events
@events.route("/")
# @logged_in
def get_all_events():

    search_query = request.args.get("q")
    events = []

    with engine.connect() as conn:

        if search_query:

            query = text("SELECT * FROM event WHERE name LIKE :query")
            params = {"query": f"%{search_query}%"}
            result = conn.execute(query, params)
            # Assuming db is your SQLAlchemy database instance
            result = result.fetchall() 
            for row in result:
                events.append(dict(row._mapping))
                print(row)
            response = jsonify(FETCHED_EVENTS, {"data": events})
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 200
            return response
        else:
            query = text("SELECT * FROM event")
            params = {}
            result = conn.execute(query, params).fetchall()

            if not result:
                response = jsonify(NO_EVENTS)
                response.headers.add("Access-Control-Allow-Origin", "*")
                response.status_code = 404
                return response
            else:

                for row in result:

                    events.append(dict(row._mapping))
                    response = jsonify(FETCHED_EVENTS, {"data": events})
                    response.headers.add("Access-Control-Allow-Origin", "*")
                    response.status_code = 200
                return response


@events.route("/<event_organizer_id>")
# @logged_in
def get_all_events_by_organizer(event_organizer_id):

    events = []

    with engine.connect() as conn:

        query = text("SELECT * FROM event WHERE event_organizer_id = :e_id")
        params = dict(e_id=event_organizer_id)
        result = conn.execute(query, params).fetchall()

        if "id" in session:

            response = jsonify(FETCHED_EVENTS, {"data": events})
        else:
            response = jsonify({"error": "Photographer is not logged in"})

        if not result:
            response = jsonify(NO_EVENTS)
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 404
            return response
        else:

            for row in result:

                events.append(dict(row._mapping))
                response = jsonify(FETCHED_EVENTS, {"data": events})
                response.headers.add("Access-Control-Allow-Origin", "*")
                response.status_code = 200
            return response


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
                response.status_code = 400
                return response
            else:
                response = jsonify(EVENT_RETRIEVED, {"data": dict(result._mapping)})
                response.headers.add("Access-Control-Allow-Origin", "*")
                response.status_code = 200
                return response


@events.route("/<event_organizer_id>/<id>")
# @logged_in
def get_all_events_by_organizer_by_id(event_organizer_id, id):

    events = []

    with engine.connect() as conn:

        query = text(
            "SELECT * FROM event WHERE event_organizer_id = :e_id AND id = :id"
        )
        params = dict(e_id=event_organizer_id)
        result = conn.execute(query, params).fetchall()

        if "id" in session:

            response = jsonify(FETCHED_EVENTS, {"data": events})
        else:
            response = jsonify({"error": "Photographer is not logged in"})

        if not result:
            response = jsonify(NO_EVENTS)
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 404
            return response
        else:

            for row in result:

                events.append(dict(row._mapping))
                response = jsonify(FETCHED_EVENTS, {"data": events})
                response.headers.add("Access-Control-Allow-Origin", "*")
                response.status_code = 200
            return response


@events.route("/slug/<slug>", methods={"GET"})
# @logged_in
def get_by_slug(slug):

    if request.method == "GET":
        with engine.connect() as conn:

            query = text("SELECT * FROM event where slug = :slug")
            param = dict(slug=slug)

            result = conn.execute(query, param).fetchone()
            print(result)
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


# Create events
@events.route("/<event_organizer_id>/create_event", methods=["GET", "POST"])
# @logged_in
def create_event(event_organizer_id):

    data = request.form
    event_slug = slugify(data["name"])

    if request.method == "POST":
        if not data["name"]:
            response = jsonify(EVENT_NAME_EMPTY)
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 400
            return response

        elif not data["date"]:
            response = jsonify(EVENT_DATE_EMPTY)
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 400
            return response

        folder_path = os.path.join(current_app.static_folder, "gallery", event_slug)
        os.makedirs(folder_path, exist_ok=True)

        with engine.connect() as conn:

            query = text(
                "INSERT INTO event(event_organizer_id, slug, name,date,venue,time_start,time_end,short_description,no_of_participants,datetime_created) VALUES(:e_id,:slug,:name,:date,:venue,:time_start,:time_end,:short_description,:no_of_participants,now())"
            )
            params = dict(
                e_id=event_organizer_id,
                slug=event_slug,
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
                response = jsonify(EVENT_SUCCESS)
                response.headers.add("Access-Control-Allow-Origin", "*")
                response.status_code = 201
                return response
            else:
                response = jsonify(EVENT_FAILED)
                response.headers.add("Access-Control-Allow-Origin", "*")
                response.status_code = 400
                return response


# Update Event
@events.route("/<event_organizer_id>/update_event/<event_id>", methods=["PUT"])
def update_event(event_organizer_id, event_id):

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
            "UPDATE event SET name = :name, date = :date, venue = :venue, time_start = :time_start, time_end = :time_end, short_description = :short_description, no_of_participants = :no_of_participants, status = :status WHERE event_organizer_id = :e_id AND id = :id"
        )

        params = dict(
            id=event_id,
            e_id=event_organizer_id,
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
            response.status_code = 200
            return response
        else:
            response = jsonify(FAILED_UPDATE)
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 400
            return response


# Delete Event
@events.route("<event_organizer_id>/delete_event/<event_id>", methods=["DELETE"])
def delete_event(event_id, event_organizer_id):

    with engine.connect() as conn:

        query = text("DELETE from event WHERE event_organizer_id = :e_id AND id = :id")
        params = dict(id=event_id, e_id=event_organizer_id)

        result = conn.execute(query, params)

        conn.commit()

        if result.rowcount > 0:
            response = jsonify(DELETED_EVENT)
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 200
            return response
        else:
            response = jsonify(FAILED_DELETE)
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 400
            return response
