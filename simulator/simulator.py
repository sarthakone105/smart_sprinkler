import requests
import random
import time


API_URL = "http://127.0.0.1:5001/moisture"


while True:
    moisture = random.randint(1500, 3000)
    print(f"Sending simulated moisture: {moisture}")
    
    try:
        response = requests.post(API_URL, json={"moisture": moisture})
        print(response.status_code, response.text)
    except Exception as e:
        print("Error sending data:", e)
        
    time.sleep(3)