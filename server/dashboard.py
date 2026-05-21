from flask import (
    Flask,
    render_template
)

import requests
from requests.exceptions import RequestException

app = Flask(__name__)

@app.route("/")
def dashboard():

    error = None
    data = {
        "received": 0,
        "completed": 0,
        "failed": 0,
        "processing": [],
        "completed_tasks": [],
        "failed_tasks": []
    }

    try:
        response = requests.get(
            "http://127.0.0.1:8080/status",
            timeout=3
        )
        response.raise_for_status()
        data = response.json()
    except RequestException as exc:
        error = (
            "Tidak dapat menghubungi server status di localhost:8080. "
            "Pastikan backend berjalan terlebih dahulu. "
            f"({exc})"
        )

    return render_template(
        "dashboard.html",
        data=data,
        error=error
    )

if __name__ == "__main__":

    app.run(
        port=5000,
        debug=True
    )