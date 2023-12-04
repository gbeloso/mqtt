import paho.mqtt.client as mqtt
import json
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

mqtt_broker = "localhost"
mqtt_topic = "environmental_monitoring"
mqtt_username = "test_user"
mqtt_password = "test_user"

# Armazenar os dados recebidos por IP
last_data_by_ip = {}
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    # print(f"Received message: {payload}")

    # Armazenar o último conjunto de dados para o IP específico
    last_data_by_ip[payload["ip"]] = payload

    map_ip = list(last_data_by_ip)

    data_to_send = {
        'ips': map_ip,
        'msg': last_data_by_ip
    }

    # for ip in data_to_send['ips']:
    #     print(f'ip: {ip}')
    #     print(f'{data_to_send["msg"][ip]["ip"]}')
    #     print(f'{data_to_send["msg"][ip]["localization"]}')
    #     print(f'{data_to_send["msg"][ip]["soil_moisture"]}')
    #     print(f'{data_to_send["msg"][ip]["temperature"]}')
    #     print(f'{data_to_send["msg"][ip]["humidity"]}')
    #     print(f'{data_to_send["msg"][ip]["leaf_temperature"]}')
    #     print('\n')
        
    # print('\n\n')

    
    # Emitir os dados mais recentes para o cliente
    socketio.emit("update_data", last_data_by_ip)

mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(mqtt_username, mqtt_password)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    mqtt_client.connect(mqtt_broker, 1883, 60)
    mqtt_client.loop_start()
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
