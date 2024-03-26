from flask import Flask, jsonify, request, render_template
from event_organizer.event_organizer import event_organizer
from event.events import events
from photographer.photographer import photographer

app = Flask(__name__)

# blue_prints
app.register_blueprint(event_organizer, url_prefix="/event_organizer")
app.register_blueprint(events, url_prefix="/events")
app.register_blueprint(photographer, url_prefix="/photographer")


# Routes
@app.route("/")
def index():
    return render_template("index.js")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
