from flask import Flask, render_template
from event_organizer.event_organizer import event_organizer
from event.events import events
from photographer.photographer import photographer
from runner.runners import runners
from auth.auth import auth
import uuid
from flask_cors import CORS

app = Flask(__name__)

app.config["SECRET_KEY"] = uuid.uuid4().hex

CORS(app)
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
