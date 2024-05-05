import os
from flask import jsonify, current_app, Blueprint, request, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
from bib_recog.copy_of_racebib import images
from photographer.photographer import get_by_id

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


@upload_images.route("/", methods=["POST","GET"])
def multi_images():
    if request.method == "POST":
        photographer_id = request.args.get('photog_id')
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

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Construct the upload path based on event slug and photographer ID
                upload_folder = os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    event_slug,
                    str(photographer_id),
                )
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                file.save(os.path.join(upload_folder, filename))

        response = jsonify({"success": True, "message": "Uploaded successfully"})
        response.headers.add("Allow-Access-Control-Origin", "*")
        response.status_code = 201
        return response

    if request.method == "GET":

        event_slug = request.args.get("slug")
        photog_id = request.args.get("photog_id")
        query = request.args.get("query")
        folderpath = event_slug+"/"+photog_id
        filenames = images(folderpath, query)
        response_data = {
            "success": True,
            "message": "Fetched successfully",
            "data": filenames,
        }

        response = jsonify(response_data)
        response.headers.add("Allow-Access-Control-Origin", "*")
        response.status_code = 200
        return response
