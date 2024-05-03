import os
from flask import jsonify, current_app, Blueprint, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from bib_recog.copy_of_racebib import images


upload_images = Blueprint("upload", __name__)
CORS(upload_images)


ALLOWED_EXTENSIONS = set(["txt", "pdf", "png", "jpg", "jpeg", "gif"])


def initialize_upload_folder():
    path = os.getcwd()
    UPLOAD_FOLDER = os.path.join(path, "gallery")

    if not os.path.isdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)

    current_app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    current_app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


@upload_images.before_app_request
def before_first_request_func():
    initialize_upload_folder()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_images.route("/", methods=["GET", "POST"])
def multi_images():

    if request.method == "POST":

        if "files[]" not in request.files:

            response = jsonify(
                {"success": False, "message": "not located in the folder"}
            )
            response.headers.add("Allow-Access-Control-Origin", "*")
            return response, 404

        files = request.files.getlist("files[]")

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))

        response = jsonify({"success": True, "message": "Uploaded successfully"})
        response.headers.add("Allow-Access-Control-Origin", "*")
        return response, 201

    if request.method == "GET":

        event_slug = request.args.get("event_slug")
        query = request.args.get("query")

    filenames = images(event_slug, query)
    response_data = {
        "success": True,
        "message": "Fetched successfully",
        "data": filenames,
    }

    response = jsonify(response_data)
    response.headers.add("Allow-Access-Control-Origin", "*")
    return response, 301
