from database import engine
from sqlalchemy import text, exc
from flask import Blueprint, request, jsonify
from strings import *


class photographer_obj:
    def __init__(self, event_organizer_id, name, address, email, password, status):

        self.event_orgainzer_id = event_organizer_id
        self.name = name
        self.address = address
        self.email = email
        self.password = password
        self.status = status


photographer = Blueprint("photographers", __name__)


@photographer.route("<event_organizer_id>/registration", methods=["GET", "POST"])
def register_photographer(event_organizer_id):

    data = request.form

    if request.method == "POST":
        if data["name"] is None:
            return jsonify(NAME_EMPTY), 404
        elif data["address"] is None:
            return jsonify(ADDRESS_EMPTY), 404
        elif data["email"] is None:
            return jsonify(EMAIL_EMPTY), 404
        elif data["status"] is None:
            return jsonify(STATUS_EMPTY), 404

        with engine.connect() as conn:
            query = text(
                "INSERT INTO photographer(event_organizer_id, name, address, email, status) VALUES(:event_organizer_id, :name, :address, :email, :status)"
            )

            params = dict(
                event_organizer_id=event_organizer_id,
                name=data["name"],
                address=data["address"],
                email=data["email"],
                status=data["status"],
            )

            conn.execute(query, params)

            conn.commit()
        return jsonify(PHOTOGRAPHER_REGISTERED_SUCCESSFULLY), 201
