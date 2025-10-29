import os


LOG_FILE = "logs/pump_log.txt"
DRY_THRESHOLD = 2500
WET_THRESHOLD = 1800

pump_on = False


def process_moisture(moisture, timestamp):
    
    global pump_on
    
    if moisture is None:
        return "INVALID"
    
    if moisture > DRY_THRESHOLD and not pump_on:
        
        pump_on = True
        status = "ON"
        
    elif moisture < WET_THRESHOLD and pump_on:
        pump_on = False
        status = "OFF"
        
    else:
        status = "NO CHANGE"
    
    
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} | Moisture: {moisture} | Pump: {status}\n")
        
    print(f"[{timestamp}] Moisture={moisture}, Pump={status}")
    return status