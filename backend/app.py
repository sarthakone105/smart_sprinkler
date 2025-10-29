from flask import Flask, request, jsonify
import datetime
from controller import process_moisture


app = Flask(__name__)



@app.route("/moisture", methods=["POST"])
def receive_moisture():
    
    # data = request.get_json()
    data = request.get_json()
    moisture = data.get('moisture')
    timestamp = datetime.datetime.now()
    
    status = process_moisture(moisture, timestamp)
    
    return jsonify({"message": "Data received", "pump_status": status})


if __name__ == "__main__":
    app.run(debug=True, port=5001)