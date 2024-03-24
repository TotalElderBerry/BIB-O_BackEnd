from flask import Flask, jsonify, request, render_template
from event_organizer.event_organizer import event_organizer

app = Flask(__name__)

# blue_prints
app.register_blueprint(event_organizer, url_prefix="/event_organizer")


# Routes
@app.route("/")
def index():
    return render_template("index.js")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
