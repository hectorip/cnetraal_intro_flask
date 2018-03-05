from flask import Flask, request, jsonify
import requests
import json
from bot import send_message

app = Flask(__name__)

@app.route("/fb_webhook", methods=["GET", "POST"])
def fb_webhook():
    if request.method == "GET":
        my_token = "holicrayoli"
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if my_token == verify_token:
            return challenge
        else:
            return "Fallaste"
    elif request.method == "POST":
        if send_message():
            return "Funciona"
        else: 
            return "Fallamos"


@app.route("/", methods=["GET", "POST"])
def index():
    data = json.loads(request.data)
    age = int(data.get("results").get("age").get("value"))
    if age >= 18:
        response = {"approved": "true"}
    else:
        response = {"approved": "false"}
    return jsonify(response)

if __name__ == "__main__":
    app.run(
        port=5001,
        debug=True
    )
