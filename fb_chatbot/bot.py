import requests
import json
from flask import request


def get_messaging(body):
    entries = body.get("entry")  # Esto devuelve unsa colección
    messaging = entries[0].get("messaging")  # Esto es un dict
    return messaging

def get_sender_id(body):
    messaging = get_messaging(body)
    sender = messaging[0].get("sender")

    return sender.get("id")


def get_user_message(body):
    messaging = get_messaging(body)
    message = messaging[0].get("message")
    return message.get("text")


def send_fb_message(message, fbid):
    PAGE_ACCESS_TOKEN = "<access_token>"
    fb_url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + PAGE_ACCESS_TOKEN
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


def get_intent(message):
    # Mandar a request a DialogFlow
    access_token = "<dialogFlow-token>"
    url = "https://dialogflow.googleapis.com/v2beta1/projects/flasker-19fbd/agent/sessions/MYSESSION:detectIntent"
    # Obtener intent de respuesta de DialogFlow
    data = {
        "queryInput": {
            "text": {
                "text": message,
                "languageCode": "es-419"
            }
        }
    }
    response = requests.post(url, json=data, headers={
                             'Authorization': 'Bearer ' + access_token})  # sacar el body de la respuesta
    body = json.loads(response.text)
    intent = body.get("queryResult").get("intent").get("displayName")
    return intent


def get_next_message(body):
    # Mandar el mensaje a DialogFlow y obtener el intent
    response = ""
    user_message = get_user_message(body)
    intent = get_intent(user_message)
    if intent == "greeting":
        response = "Hola, soy UN BOT 🤖"
    else:
        response = "No te entendí. 🤔"
    # Escoger un mensaje adecuado para el intent

    return response


def send_message():
    body = json.loads(request.data)
    fbid = get_sender_id(body)
    message = get_next_message(body)
    return send_fb_message(message, fbid)