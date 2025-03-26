  

import requests
import time
import random

url = "http://localhost:3000/predict"

while True:
simulated_value = random.uniform(40, 100) # Generate random data
response = requests.post(url, json={"value": simulated_value})
print(response.json())

time.sleep(2) # Sending the data for every 2 seconds
