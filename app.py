from flask import Flask, Response, request, session
from event_organizer.event_organizer import event_organizer
from event.events import events
from photographer.photographer import photographer
from runner.runners import runners
from auth.auth import auth
from flask_cors import CORS
from upload.upload import upload_images
import uuid

app = Flask(__name__, static_url_path="/static")

# Configurations
app.config["SECRET_KEY"] = uuid.uuid4().hex
app.config["CORS_HEADERS"] = "Content-Type"


CORS(app)


@app.before_request
def before_request_func():
    if request.method == "OPTIONS":
        return Response()


# blue_prints
app.register_blueprint(event_organizer, url_prefix="/event_organizer")
app.register_blueprint(events, url_prefix="/event")
app.register_blueprint(photographer, url_prefix="/photographer")
app.register_blueprint(runners, url_prefix="/runner")
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(upload_images, url_prefix="/")


# Routes
@app.route("/")
def index():
    return "Hello world"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
