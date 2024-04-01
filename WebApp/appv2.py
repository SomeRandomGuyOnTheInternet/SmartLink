from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
#import flask.socketio import SocketIO

app = Flask(__name__)

# MQTT Configuration
MQTT_BROKER_URL = "192.168.18.79"
MQTT_BROKER_PORT = 1883
BROKER_ADDRESS = "localhost"
MQTT_KEEPALIVE_INTERVAL = 5
CONNECT_REMOTE_REQUEST = "smartlink/connect_remote_request"
CONNECT_REMOTE_RESPONSE = "smartlink/connect_remote_response"
LEARN_COMMAND_REQUEST = "smartlink/learn_command_request" 
LEARN_COMMAND_RESPONSE ="smartlink/learn_command_response"
SEND_COMMAND_REQUEST = "smartlink/send_command_reguest"
SEND_COMMAND_RESPONSE = "smartlink/send_command_response"

def on_connect(client, userdata, flags, rc):
	#Subscribe to a the Topic
	mqttc.subscribe(CONNECT_REMOTE_RESPONSE, 0)
	mqttc.subscribe(LEARN_COMMAND_RESPONSE, 0)
	mqttc.subscribe(SEND_COMMAND_RESPONSE, 0)
	
# Define on_subscribe event Handler
def on_subscribe(client, userdata, mid, granted_qos):
	print("Subscribed to MQTT Topic "+CONNECT_REMOTE_RESPONSE)
	print("Subscribed to MQTT Topic "+LEARN_COMMAND_RESPONSE)
	print("Subscribed to MQTT Topic "+SEND_COMMAND_RESPONSE)

# Callback function for when a PUBLISH message is received from the server.
def on_message(client, userdata, message):
	print(f"Message received on topic {message.topic}: {str(message.payload.decode('utf-8'))}")   
	if message.topic == CONNECT_REMOTE_RESPONSE:
		print("Processing CONNECT_REMOTE_RESPONSE message and publishing a response..")
		response_payload={"status": "ok"}
		client.publish(CONNECT_REMOTE_REQUEST,json.dumps(response_payload))
	if message.topic == LEARN_COMMAND_RESPONSE:
		print("Processing LEARN_COMMAND_RESPONSE message and publishing a response..")
		response_payload={"status": "ok"}
		client.publish(LEARN_COMMAND_REQUEST ,json.dumps(response_payload))
	if message.topic == SEND_COMMAND_RESPONSE:
		print("Processing SEND_COMMAND_RESPONSE message and publishing a response..")
		response_payload={"status": "ok"}
		client.publish(SEND_COMMAND_REQUEST ,json.dumps(response_payload))
    
# Initiate MQTT Client
mqttc = mqtt.Client()
    
    
# Register Event Handlers
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# Connect with MQTT Broker
mqttc.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT, MQTT_KEEPALIVE_INTERVAL )

# Continue the network loop
mqttc.loop_start()


def on_message_found_remote(mqttc, obj, msg):
	payload = json.loads(msg.payload)
	print("Found remote!")
	print(payload)
	
def on_message_found_command(mqttc, obj, msg):
	payload = json.loads(msg.payload)
	print("Found command!")
	print(payload)

def on_subscribe(mqttc, obj, mid, reason_code_list, properties):
	print("Subscribed: " + str(mid) + " " + str(reason_code_list))
	
def publish_message(topic, message, broker_address="localhost"):
    publish.single(topic, message, hostname=broker_address)


	
# Route for serving the HTML
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find_remote', methods=['POST'])
def find_remote():
    publish_message(CONNECT_REMOTE_REQUEST, None)
    return jsonify({"success": True})
    
@app.route('/learn_command', methods=['POST'])
def learn_command():
    publish_message(LEARN_COMMAND_REQUEST, None)
    return jsonify({"success": True})
	
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0',port=5000)

