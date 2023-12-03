import paho.mqtt.client as mqtt
import json
import time
import random
import socket
import os

endpoint = os.environ.get("ENDPOINT", "localhost")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print(f"Connection failed with code {rc}")

def on_publish(client, userdata, mid):
    print("Message Published")

client = mqtt.Client()
client.username_pw_set(username="test_user", password="test_user")
client.on_connect = on_connect
client.on_publish = on_publish

client.connect(endpoint, 1883, 60)

client.loop_start()
while not client.is_connected():
    time.sleep(1)

topic = "environmental_monitoring"
localization = str(random.randint(14, 15)) + " " + str(random.randint(0, 60)) + " " + str(random.randint(0, 60)) + " " + "S, " + str(random.randint(57, 58)) + " " + str(random.randint(0, 60)) + " " + str(random.randint(0, 60)) + " " + "W"

try:
    while True:
        soil_moisture = str(random.uniform(20, 60)) 
        temperature = str(random.uniform(24, 34))
        humidity = str(random.uniform(38.8, 78.4))
        leaf_temperature = str(random.uniform(20, 29))
        data = {
            "ip": str(socket.gethostbyname(socket.gethostname())),
            "localization": localization,
            "soil_moisture": soil_moisture,
            "temperature": temperature,
            "humidity": humidity,
            "leaf_temperature": leaf_temperature
        }
        json_data = json.dumps(data)  # Serialize the data to JSON
        client.publish(topic, json_data)
        print(f"Published JSON message: {json_data}")

        time.sleep(5)  # Wait for 5 seconds before publishing the next message

except KeyboardInterrupt:
    # Disconnect from the broker when the program is interrupted
    client.disconnect()
