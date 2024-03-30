from database import engine
from flask import Blueprint, session, request, jsonify
from strings import (
    FIRST_NAME_EMPTY,
    LAST_NAME_EMPTY,
    BIB_NO_EMPTY,
    RUNNER_REGISTRATION_SUCCESSFUL,
    NO_RUNNERS,
    NO_SINGLE_RUNNER,
)
from sqlalchemy import text, exc


runners = Blueprint("runners", __name__)


@runners.route("/")
def get_all_runners():

    runners = []
    with engine.connect() as conn:

        query = text("SELECT * FROM runner")

        result = conn.execute(query)

        if not result:
            return jsonify(NO_RUNNERS)

        else:
            for row in result:
                runners.append(dict(row._mapping))

                return jsonify(runners)


@runners.route("/<id>")
def get_one_runner(id):

    with engine.connect() as conn:

        query = text("SELECT * FROM runner where id = :id")
        params = dict(id=id)

        result = conn.execute(query, params).fetchone()

        output = NO_SINGLE_RUNNER if result is None else dict(result)

        return jsonify(output)


@runners.route("/<event_id>/registration", methods=["GET", "POST"])
def registration(event_id):

    error = None

    if request.method == "POST":

        data = request.form

        if not data["first_name"]:
            return jsonify(FIRST_NAME_EMPTY)
        elif not data["last_name"]:
            return jsonify(LAST_NAME_EMPTY)
        elif not data["bib_no"]:
            return jsonify(BIB_NO_EMPTY)

        with engine.connect() as conn:

            query = text(
                "INSERT INTO runner(event_id,last_name,first_name,bib_no) VALUES (:event_id,:ln, :fn, :bib)"
            )
            params = dict(
                event_id=event_id,
                ln=data["last_name"],
                fn=data["first_name"],
                bib=data["bib_no"],
            )

            conn.execute(query, params)
            conn.commit()

            return jsonify(RUNNER_REGISTRATION_SUCCESSFUL), 201


# update

# delete
