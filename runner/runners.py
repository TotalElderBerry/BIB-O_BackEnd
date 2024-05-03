from database import engine
from flask import Blueprint, session, request, jsonify
from strings import *
from sqlalchemy import text

# from auth.auth import logged_in

runners = Blueprint("runners", __name__)


@runners.route("/<event_id>")
# @logged_in
def get_all_runners(event_id):

    runners = []
    with engine.connect() as conn:

        query = text("SELECT * FROM runner WHERE event_id = :event_id")
        params = dict(event_id=event_id)
        result = conn.execute(query, params)

        if not result:
            response = jsonify(NO_RUNNERS)
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 404
            return response

        else:
            for row in result:
                runners.append(dict(row._mapping))

                response = jsonify(RUNNERS_FETCHED, {"data": runners})
                response.headers.add("Access-Control-Allow-Origin", "*")
                response.status_code = 200
                return response


@runners.route("/<event_id>/<id>")
# @logged_in
def get_one_runner(id, event_id):

    with engine.connect() as conn:

        query = text("SELECT * FROM runner where id = :id AND event_id = event_id")
        params = dict(id=id, event_id=event_id)

        result = conn.execute(query, params).fetchone()

        if result is None:
            response = jsonify(NO_SINGLE_RUNNER)
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 404
            return response

        else:
            response = jsonify(ONE_RUNNER_FETHCED, {"data": dict(result)})
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 200
            return response


# @logged_in
@runners.route("/<event_id>/registration", methods=["GET", "POST"])
def registration(event_id):

    if request.method == "POST":

        data = request.form

        if not data["first_name"]:
            response = jsonify(FIRST_NAME_EMPTY)
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 400
            return response

        elif not data["last_name"]:
            response = jsonify(LAST_NAME_EMPTY)
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 400
            return (response,)

        elif not data["bib_no"]:
            response = jsonify(BIB_NO_EMPTY)
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 400
            return (response,)

        with engine.connect() as conn:

            query_no_participants = text(
                "SELECT no_of_participants, current_no_of_participants FROM event WHERE id = :id"
            )
            params = dict(id=event_id)

            query_result = conn.execute(query_no_participants, params).fetchone()

            if query_result is None:

                response = jsonify(NO_SINGLE_RUNNER)
                response.headers.add("Access-Control-Allow-Origin", "*")
                response.status_code = 404
                return response

            else:
                no_of_participants, current_no_of_participants = query_result

                if current_no_of_participants <= no_of_participants:

                    query = text(
                        "INSERT INTO runner(event_id,last_name,first_name,bib_no, datetime_created) VALUES (:event_id,:ln, :fn, :bib, now())"
                    )
                    params = dict(
                        event_id=event_id,
                        ln=data["last_name"],
                        fn=data["first_name"],
                        bib=data["bib_no"],
                    )

                    result = conn.execute(query, params)

                    if result.rowcount > 0:

                        update_query = text(
                            "UPDATE event SET current_no_of_participants = current_no_of_participants + 1 WHERE id = :event_id"
                        )
                        params = dict(event_id=event_id)
                        result = conn.execute(update_query, params)
                        conn.commit()

                        response = jsonify(RUNNER_REGISTRATION_SUCCESSFUL)
                        response.headers.add("Access-Control-Allow-Origin", "*")
                        response.status_code = 201
                        return response

                elif current_no_of_participants > no_of_participants:

                    response = jsonify(MAX_REGISTRATION)
                    response.headers.add("Access-Control-Allow-Origin", "*")
                    response.status_code = 200
                    return response
                else:
                    response = jsonify(RUNNER_REGISTRATION_FAILED)
                    response.headers.add("Access-Control-Allow-Origin", "*")
                    response.status_code = 400
                    return response


# Update Event
@runners.route("/update_runner/<event_id>/<id>", methods=["PUT"])
def update_runner(event_id, id):

    data = request.form

    with engine.connect() as conn:

        query = text(
            "UPDATE runner SET last_name = :lname, first_name = :fname, bib_no = :bib WHERE event_id = :e_id AND id = :id"
        )

        params = dict(
            id=id,
            e_id=event_id,
            lname=data["last_name"],
            fname=data["first_name"],
            bib=data["bib_no"],
        )
        result = conn.execute(query, params)

        conn.commit()
        if result.rowcount > 0:

            response = jsonify(UPDATED_RUNNER)
            response.headers.add("Access-Control-Allow-Origin", "*")

            response.status_code = 200
            return response

        else:
            response = jsonify(FAILED_UPDATE)
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 400
            return response


runners.route("/delete_runner/<event_id>/<id>")


def delete_runner(event_id, id):

    with engine.connect() as conn:

        query = text("DELETE FROM runner WHERE event_id = :e_id AND id = :id")
        params = dict(id=id, e_id=event_id)

        result = conn.execute(query, params)

        conn.commit()

        if result.rowcount > 0:

            response = jsonify(DELETED_RUNNER)
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 400
            return response
        else:

            response = jsonify(FAILED_DELETE_RUNNER)
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 400
            return response
