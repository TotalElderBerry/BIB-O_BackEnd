from database import engine
from flask import Blueprint, session, request, jsonify
from strings import *
from sqlalchemy import text

# from auth.auth import logged_in

runners = Blueprint("runners", __name__)


@runners.route("/")
def get_all():

    runners = []
    with engine.connect() as conn:

        query = text("SELECT * FROM runner")

        result = conn.execute(query)

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


@runners.route("/<event_id>")
# @logged_in
def get_all_runners(event_id):

    runner_status = request.args.get("status")
    runners = []
    with engine.connect() as conn:

        query = text(
            "SELECT * FROM event_registration INNER JOIN runner on runner.id = runner_id WHERE event_id = :event_id AND status LIKE :status"
        )
        params = dict(event_id=event_id, status=f"%{runner_status}%")
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


@runners.route("/<id>")
# @logged_in
def get_runner_by_id(id):

    with engine.connect() as conn:

        query = text("SELECT * FROM runner where id = :id ")
        params = dict(id=id)

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


@runners.route("/<runner_id>/register_event/<event_id>", methods=["GET", "POST"])
def register_event(runner_id, event_id):

    data = request.form

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
                    "INSERT INTO event_registration(runner_id , event_id, category, datetime_created) VALUES (:r_id, :e_id, :category, now())"
                )
                params = dict(r_id=runner_id, e_id=event_id, category=data["category"])

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


# @logged_in
@runners.route("/registration", methods=["GET", "POST"])
def registration():

    if request.method == "POST":

        data = request.form

        with engine.connect() as conn:

            query = text(
                "INSERT INTO runner(last_name, first_name, email, password, datetime_created) VALUES (:ln, :fn, :email, :password, now())"
            )
            params = dict(
                ln=data["last_name"],
                fn=data["first_name"],
                email=data["email"],
                password=data["password"],
            )

            result = conn.execute(query, params)

            conn.commit()

            if result.rowcount > 0:

                response = jsonify(
                    {"success": True, "message": "Runner successfully registered!"}
                )
                response.headers.add("Access-Control-Allow-Origin", "*")
                response.status_code = 200

                return response
            else:

                response = jsonify({"success": False, "message": "Unable to register"})
                response.headers.add("Access-Control-Allow-Origin", "*")
                response.status_code = 400

                return response


# Update Event
@runners.route("/update_runner/<id>", methods=["PUT"])
def update_runner(event_id, id):

    data = request.form

    with engine.connect() as conn:

        query = text(
            "UPDATE runner SET last_name = :lname, first_name = :fname, email = :email, password = :password WHERE id = :id"
        )

        params = dict(
            id=id,
            e_id=event_id,
            lname=data["last_name"],
            fname=data["first_name"],
            email=data["email"],
            password=data["password"],
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


runners.route("/delete_runner/<id>")


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
