from flask import Flask, request
import requests
import json

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
    PAGE_ACCESS_TOKEN = "EAADAic8CH4cBAIYFa88rsBzvWNqPkYyXfwomoLGOX0yyHTRLP1bEkSlSOCuOWcgjY7xJ1hfZAuJGEZA8j2ZBbjfy3QZC2KHkm6ZCgwYk09Qg3e4B7uiKKWWFplaTCmQZB4nyhoZAlAtRsI6BNshJzq4SQe6ixrZAdlk7dyZCLgzWPRQZDZD"
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


if __name__ == "__main__":
    app.run(
        port=5001,
        debug=True
    )
