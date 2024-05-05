import os
from flask import jsonify, current_app, Blueprint, request, session
from flask_cors import CORS
from sqlalchemy import text
from werkzeug.utils import secure_filename
from bib_recog.copy_of_racebib import images,generate
from photographer.photographer import get_by_id
from database import engine
from strings import *

upload_images = Blueprint("upload", __name__)
CORS(upload_images)


ALLOWED_EXTENSIONS = set(["txt", "pdf", "png", "jpg", "jpeg", "gif"])


def initialize_upload_folder():
    path = os.getcwd()
    UPLOAD_FOLDER = os.path.join(path, "static/gallery")

    if not os.path.isdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)

    current_app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    current_app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


@upload_images.before_app_request
def before_first_request_func():
    initialize_upload_folder()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_images.route("/", methods=["POST", "GET"])
def multi_images():
    if request.method == "POST":
        photographer_id = request.args.get("photog_id")
        event_id = request.args.get("event_id")
        event_slug = request.args.get("slug")

        if not event_slug:
            response = jsonify({"success": False, "message": "Event slug not provided"})
            response.headers.add("Allow-Access-Control-Origin", "*")
            response.status_code = 400
            return response

        if not photographer_id:
            response = jsonify(
                {"success": False, "message": "Photographer ID not found in session"}
            )
            response.headers.add("Allow-Access-Control-Origin", "*")
            response.status_code = 400
            return response

        if "files[]" not in request.files:
            response = jsonify({"success": False, "message": "Files not found"})
            response.headers.add("Allow-Access-Control-Origin", "*")
            return response, 404

        files = request.files.getlist("files[]")
        total_uploaded = len(files)
        upload_folder = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            event_slug,
            str(photographer_id),
        )
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Construct the upload path based on event slug and photographer ID
                file.save(os.path.join(upload_folder, filename))

        with engine.connect() as conn:

            query_fetch = text(
                "SELECT * FROM uploader WHERE photographer_id = :p_id AND event_id = :e_id"
            )
            params_fetch = dict(p_id=photographer_id, e_id=event_id)
            result_query = conn.execute(query_fetch, params_fetch).fetchone()

            if result_query is None:

                query_upload = text(
                    "INSERT INTO uploader(photographer_id, event_id, number_of_uploads) VALUES (:p_id, :e_id, :no_uploads)"
                )
                params = dict(
                    p_id=photographer_id, e_id=event_id, no_uploads=total_uploaded
                )
                result = conn.execute(query_upload, params)
                conn.commit()

                if result.rowcount > 0:

                    response = jsonify(UPLOADER_INSERTED)
                    response.headers.add("Access-Control-Allow-Origin", "*")
                    response.status_code = 201
            else:
                query_update = text(
                    "UPDATE uploader "
                    "SET number_of_uploads = number_of_uploads + :no_uploads "
                    "WHERE photographer_id = :p_id AND event_id = :e_id"
                )
                params_update = dict(
                    p_id=photographer_id, e_id=event_id, no_uploads=total_uploaded
                )
                result_update = conn.execute(query_update, params_update)
                conn.commit()

                if result_update.rowcount > 0:
                    response = jsonify(UPLOADER_UPDATED)
                    response.headers.add("Access-Control-Allow-Origin", "*")
                    response.status_code = 200

        generate(event_slug,str(photographer_id),files)
        response = jsonify({"success": True, "message": "Uploaded successfully"})
        response.headers.add("Allow-Access-Control-Origin", "*")
        response.status_code = 201
        return response

    if request.method == "GET":

        event_slug = request.args.get("slug")
        photog_id = request.args.get("photog_id")
        query = request.args.get("query")
        if(photog_id):
            filenames = images(event_slug, query,photog_id)
        else:    
            filenames = images(event_slug, query)
        response_data = {
            "success": True,
            "message": "Fetched successfully",
            "data": filenames,
        }

        response = jsonify(response_data)
        response.headers.add("Allow-Access-Control-Origin", "*")
        response.status_code = 200
        return response


@upload_images.route("/uploader", methods=["GET"])
def uploaders_per_event():
    event_id = request.args.get("event_id")
    uploaders = []

    with engine.connect() as conn:
        query = text("SELECT * FROM uploader WHERE event_id = :e_id")
        params = {"e_id": event_id}

        result = conn.execute(query, params).fetchall()

        if not result:  # Check if result is empty (no uploads)
            response = jsonify(
                {"success": False, "message": "No uploads as of the moment!"}
            )
            response.headers.add("Allow-Access-Control-Origin", "*")
            response.status_code = 404
            return response
        else:
            for row in result:
                uploaders.append(dict(row._mapping))

            response = jsonify(
                {"success": True, "message": "Uploaders found", "data": uploaders}
            )
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.status_code = 200
            return response
