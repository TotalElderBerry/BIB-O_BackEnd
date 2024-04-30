import os
from flask import Flask, Response, jsonify, request
from event_organizer.event_organizer import event_organizer
from event.events import events
from photographer.photographer import photographer
from runner.runners import runners
from auth.auth import auth
import uuid
from flask_cors import CORS
from werkzeug.utils import secure_filename
from bib_recog.copy_of_racebib import images

app = Flask(__name__, static_url_path="/static")

# Configurations
app.config["SECRET_KEY"] = uuid.uuid4().hex
app.config["CORS_HEADERS"] = "Content-Type"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

# Allowed Extensions
ALLOWED_EXTENSIONS = set(["txt", "pdf", "png", "jpg", "jpeg", "gif"])


CORS(app)


@app.before_request
def before_request_func():
    if request.method == "OPTIONS":
        return Response()


# Get current path
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, "uploads")

# Make directory if uploads is not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# blue_prints
app.register_blueprint(event_organizer, url_prefix="/event_organizer")
app.register_blueprint(events, url_prefix="/event")
app.register_blueprint(photographer, url_prefix="/photographer")
app.register_blueprint(runners, url_prefix="/runner")
app.register_blueprint(auth, url_prefix="/admin")


# Routes
@app.route("/")
def index():
    return "Hello world"


@app.route("/", methods=["GET", "POST"])
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
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

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


# @app.route("/fetch")
# def fetch():
#     event_slug = request.args.get("event_slug")
#     query = request.args.get("query")
#     filenames = images(event_slug, query)
#     response_data = {
#         "success": True,
#         "message": "Fetched successfully",
#         "data": filenames,
#     }

#     response = jsonify(response_data)
#     response.headers.add("Allow-Access-Control-Origin", "*")
#     return response, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
