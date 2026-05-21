from flask import (
    Flask,
    render_template
)

import requests

app = Flask(__name__)

@app.route("/")
def dashboard():

    response = requests.get(
        "http://localhost:8080/status"
    )

    data = response.json()

    return render_template(
        "dashboard.html",
        data=data
    )

if __name__ == "__main__":

    app.run(
        port=5000,
        debug=True
    )