from flask import Flask, jsonify


app = Flask(__name__)


# Routes
@app.route("/")

def index():
    return "BIB-O bacekdn test"


@app.route("/api/bibo")

def test_json():
    return jsonify(test)

@app.route("/event_organizer/login", methods = ["GET","POST"])




if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True)