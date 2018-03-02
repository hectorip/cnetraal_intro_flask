from flask import Flask
import json

app = Flask(__name__)

@app.route("/")
def index():
    return "Hola flask!"

@app.route("/ayuda")
def help_page():
    return "Esta es la página de ayuda"

@app.route("/api/json")
def json_response():
    my_data = {
        "uno": "holi",
        "dos": "adios"
    }
    response = app.response_class(
        response=json.dumps(my_data),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == "__main__":
    app.run(port=5000, debug=True)