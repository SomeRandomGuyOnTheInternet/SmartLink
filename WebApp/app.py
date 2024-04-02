import topics
import os
import json
import socket
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
load_dotenv(override=True)

# MQTT Configuration
MQTT_BROKER_URL = os.getenv('MQTT_BROKER_URL')
MQTT_BROKER_PORT = int(os.getenv('MQTT_BROKER_PORT'))
MQTT_KEEPALIVE_INTERVAL = 5
BROKER_ADDRESS = os.getenv('BROKER_ADDRESS')
FLASK_HOSTNAME = os.getenv('FLASK_HOSTNAME')
FLASK_PORT = int(os.getenv('FLASK_PORT'))

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def on_connect(client, userdata, flags, rc):
    mqttc.subscribe(topics.CONNECT_REMOTE_RESPONSE, 0)
    mqttc.subscribe(topics.LEARN_COMMAND_RESPONSE, 0)
    mqttc.subscribe(topics.SEND_COMMAND_RESPONSE, 0)
    mqttc.message_callback_add(topics.CONNECT_REMOTE_RESPONSE, on_message_connect_remote_response)
    mqttc.message_callback_add(topics.LEARN_COMMAND_RESPONSE, on_message_learn_command_response)
    mqttc.message_callback_add(topics.SEND_COMMAND_RESPONSE, on_message_learn_command_response)

def on_subscribe(mqttc, obj, mid, reason_code_list, properties):
    print("Subscribed: " + str(mid) + " " + str(reason_code_list))

def on_message_connect_remote_response(client, userdata, message):
    print("Processing CONNECT_REMOTE_RESPONSE message and publishing a response..")
    payload = json.loads(message.payload.decode('utf-8')) 
    response_payload={"status": "ok"}
    publish_message(topics.LEARN_COMMAND_REQUEST,json.dumps(response_payload))
    
def on_message_learn_command_response(client, userdata, message):
    print("Processing LEARN_COMMAND_RESPONSE message and publishing a response..")
    payload = json.loads(message.payload.decode('utf-8')) 
    response_payload={"commmand": payload["command"]}
    print(response_payload)
    publish_message(topics.SEND_COMMAND_REQUEST ,json.dumps(response_payload))

def on_message_send_command_response(client, userdata, message):
    print("Processing SEND_COMMAND_RESPONSE message and publishing a response..")
    payload = json.loads(message.payload.decode('utf-8')) 
    
def publish_message(topic, message, broker_address=BROKER_ADDRESS):
    publish.single(topic, message, hostname=broker_address)

    
# Route for serving the HTML
@app.route('/', methods=['GET'])
def index():
    alert = request.args.get('alert')
    return render_template('index.html', alert=alert)

@app.route('/find_remote', methods=['POST'])
def find_remote():
    try:
        mqttc.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT, MQTT_KEEPALIVE_INTERVAL)
        mqttc.on_connect = on_connect
        mqttc.on_subscribe = on_subscribe
        mqttc.loop_start()
        publish_message(topics.CONNECT_REMOTE_REQUEST, None)
        return "Sent request to server to find remote.", 200
    except socket.timeout as e:
        print(e)
        return "Cannot find a remote client! Please make sure remote client is running on the same network.", 400
    
@app.route('/learn_command', methods=['POST'])
def learn_command():
    try:
        publish_message(topics.LEARN_COMMAND_REQUEST, None)
        return "Sent request to server to learn IR command.", 200
    except ConnectionRefusedError as e:
        print(e)
        return "There is no remote client to learn command from! Please make sure you have already connected with the remote client.", 400
    
@app.route('/send_command', methods=['POST'])
def send_command():
    try:
        command = request.json.get("command", "")
        payload = {"command": command}
        publish_message(topics.SEND_COMMAND_REQUEST, json.dumps(payload))
        return "Sent request to server to send IR command.", 200
    except ConnectionRefusedError as e:
        print(e)
        return "Cannot find a remote client to send command to! Please make sure remote client is running on the same network.", 400


if __name__ == '__main__':
    app.run(debug=True, host=FLASK_HOSTNAME, port=FLASK_PORT)