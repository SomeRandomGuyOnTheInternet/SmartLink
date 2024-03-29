from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json

app = Flask(__name__)

# MQTT Configuration
MQTT_BROKER_URL = "172.16.150.7"
MQTT_BROKER_PORT = 1883
BROKER_ADDRESS = "localhost"
CONNECT_REMOTE_REQUEST = "smartlink/connect_remote_request"
CONNECT_REMOTE_RESPONSE = "smartlink/connect_remote_response"
LEARN_COMMAND_REQUEST = "smartlink/learn_command_request" 
LEARN_COMMAND_RESPONSE ="smartlink/learn_command_response"
SEND_COMMAND_REQUEST = "smartlink/send_command_reguest"
SEND_COMMAND_RESPONSE = "smartlink/send_command_response"

# Callback function for when a PUBLISH message is received from the server.
def on_message(client, userdata, message):
    print(f"Message received on topic {message.topic}: {str(message.payload.decode('utf-8'))}")   
    payload = message.payload.decode('utf-8')
    
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
	

# Initialize MQTT Client
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT, 60)
mqtt_client.on_message = on_message
mqtt_client.on_subscribe = on_subscribe
print("Connecting to MQTT broker....")
mqtt_client.subscribe(CONNECT_REMOTE_RESPONSE)
mqtt_client.subscribe(LEARN_COMMAND_RESPONSE)
mqtt_client.subscribe(SEND_COMMAND_RESPONSE)
mqtt_client.message_callback_add(CONNECT_REMOTE_RESPONSE, on_message_found_remote)
mqtt_client.message_callback_add(LEARN_COMMAND_RESPONSE, on_message_found_command)
print("Connected to MQTT broker.")
mqtt_client.loop_start()

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
	
