from flask import Flask, request, jsonify
import datetime
from controller import (
    process_moisture,
    get_pump_status,
    get_latest_moisture
)

app = Flask(__name__)

@app.route("/moisture", methods=["POST"])
def receive_moisture():
    """Receive and process moisture data"""
    data = request.get_json()
    moisture = data.get("moisture")
    timestamp = datetime.datetime.now()

    status = process_moisture(moisture, timestamp)
    return jsonify({"message": "Data received", "pump_status": status})


@app.route("/status", methods=["GET"])
def get_status():
    """Return pump ON/OFF state"""
    pump_on = get_pump_status()
    return jsonify({"pump_status": "ON" if pump_on else "OFF"})


@app.route("/latest_moisture", methods=["GET"])
def latest_moisture():
    """Return latest saved moisture reading"""
    data = get_latest_moisture()
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
