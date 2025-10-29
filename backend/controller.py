import os
import json


LOG_FILE = "logs/pump_log.txt"
STATE_FILE = "config/system_state.json"

DRY_THRESHOLD = 2500
WET_THRESHOLD = 1800

def load_system_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"pump_on": False, "moisture": None, "timestamp": None}
    return {"pump_on": False, "moisture": None, "timestamp": None}


def save_system_state(pump_on, moisture, timestamp):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)

    state = {
        "pump_on": pump_on,
        "moisture": moisture,
        "timestamp": str(timestamp)
    }

    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def process_moisture(moisture, timestamp):    
    if moisture is None:
        return "INVALID"

    state = load_system_state()
    pump_on = state.get("pump_on", False)

    if moisture > DRY_THRESHOLD and not pump_on:
        pump_on = True
        status = "ON"

    elif moisture < WET_THRESHOLD and pump_on:
        pump_on = False
        status = "OFF"

    else:
        status = "NO CHANGE"


    save_system_state(pump_on, moisture, timestamp)

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} | Moisture: {moisture} | Pump: {status}\n")

    print(f"[{timestamp}] Moisture={moisture}, Pump={status}")
    return status



def get_pump_status():
    
    state = load_system_state()
    return state.get("pump_on", False)



def get_latest_moisture():
    
    state = load_system_state()
    return {
        "moisture": state.get("moisture"),
        "timestamp": state.get("timestamp")
    }
