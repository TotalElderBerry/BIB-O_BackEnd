from flask import Flask, jsonify


app = Flask(__name__)

test = [
    {
    'id' : 1,
    'name' : 'Jeremy',
    'user' : "ampats11",
    }
    
]

@app.route("/")

def index():
    return "BIB-O bacekdn test"


@app.route("/api/bibo")

def test_json():
    return jsonify(test)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True)