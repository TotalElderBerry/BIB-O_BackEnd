from flask import Flask, jsonify,request
from controllers import login, register

app = Flask(__name__)


# Routes
@app.route("/")

def index():
    return "BIB-O bacekdn test"


@app.route("/event_organizer/login", methods = ["GET","POST"])
def login_user():

    result = login()
    return result

@app.route("/event_organizer/<event_id>/registration", methods = ["GET","POST"])

def register_user():


    result = register()
    return result





if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True)