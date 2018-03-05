from flask import Flask, request, jsonify
import requests
import json
from bot import send_message

app = Flask(__name__)

def get_messaging(body):
    entries = body.get("entry")  # Esto devuelve unsa colección
    messaging = entries[0].get("messaging") # Esto es un dict
    return messaging

def get_sender_id(body):
    messaging = get_messaging(body)
    sender = messaging[0].get("sender")

    return sender.get("id")
def get_user_message(body):
    messaging = get_messaging(body)
    message = messaging[0].get("message")
    return message.get("text")

def send_message():
    PAGE_ACCESS_TOKEN = "ACCESS_TOKEN"
    fb_url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + PAGE_ACCESS_TOKEN
    body = json.loads(request.data)
    fbid = get_sender_id(body)
    message = get_user_message(body) # obtener el mensaje del usuario y repetirselo
    request_body = {
        "messaging_type": "RESPONSE",
        "recipient": {
            "id": fbid
        },
        "message": {
            "text": message
        }
    }
    response = requests.post(fb_url, json=request_body)

    if response.status_code > 399:
        print("Hubo un error al responder el mensaje")
        print(response.text)
        return False
    else:
        print("todo bien")
        return True


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
