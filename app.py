from flask import Flask, jsonify,request
from controllers.login import login

app = Flask(__name__)


# Routes
@app.route("/")

def index():
    return "BIB-O bacekdn test"


@app.route("/event_organizer/login", methods = ["GET","POST"])
def login():
    
    result = login()
    return result





if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True)