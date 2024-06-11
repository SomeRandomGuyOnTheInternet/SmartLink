import topics
import auth
import os
import json
import socket
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session, url_for
from flask_socketio import SocketIO, emit
from device import Device
from action import Action
from data_manager import DataManager

load_dotenv(override=True)
MQTT_BROKER_URL = os.getenv('MQTT_BROKER_URL')
MQTT_BROKER_PORT = int(os.getenv('MQTT_BROKER_PORT'))
MQTT_KEEPALIVE_INTERVAL = 5
APP_KEY = os.getenv('APP_KEY')
BROKER_ADDRESS = os.getenv('BROKER_ADDRESS')
FLASK_HOSTNAME = os.getenv('FLASK_HOSTNAME')
FLASK_PORT = int(os.getenv('FLASK_PORT'))

app = Flask(__name__)
app.secret_key = APP_KEY
socketio = SocketIO(app, ebgineio_logger=True, logger=True)
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
data_manager = DataManager()
data_manager.load_data()

def on_connect(self, client, userdata, flags, rc):
    mqttc.subscribe(topics.CONNECT_REMOTE_RESPONSE, 0)
    mqttc.subscribe(topics.LEARN_COMMAND_RESPONSE, 0)
    mqttc.subscribe(topics.SEND_COMMAND_RESPONSE, 0)
    mqttc.message_callback_add(topics.CONNECT_REMOTE_RESPONSE, on_message_connect_remote_response)
    mqttc.message_callback_add(topics.LEARN_COMMAND_RESPONSE, on_message_learn_command_response)
    mqttc.message_callback_add(topics.SEND_COMMAND_RESPONSE, on_message_learn_command_response)
    auth.connected = True

def on_disconnect(self, client, userdata, flags, rc):
    auth.connected = False

def on_subscribe(mqttc, obj, mid, reason_code_list, properties):
    print("Subscribed: " + str(mid) + " " + str(reason_code_list))

def publish_message(topic, payload, broker_address=BROKER_ADDRESS):
    publish.single(topic, payload, hostname=broker_address)

def on_message_connect_remote_response(client, userdata, message):
    print("Processing CONNECT_REMOTE_RESPONSE message and publishing a response..")
    payload = json.loads(message.payload.decode('utf-8'))
    socketio.emit(topics.CONNECT_REMOTE_RESPONSE, payload)
    
def on_message_learn_command_response(client, userdata, message):
    print("Processing LEARN_COMMAND_RESPONSE message and publishing a response..")
    payload = json.loads(message.payload.decode('utf-8'))
    socketio.emit(topics.LEARN_COMMAND_RESPONSE, payload)

def on_message_send_command_response(client, userdata, message):
    print("Processing SEND_COMMAND_RESPONSE message and publishing a response..")
    payload = json.loads(message.payload.decode('utf-8'))
    socketio.emit(topics.SEND_COMMAND_RESPONSE, payload)


@app.route('/find-remote', methods=["GET"])
def find_remote():
    return render_template('find-remote.html')

@app.route('/find-remote', methods=["POST"])
def find_remote_post():
    try:
        mqttc.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT, MQTT_KEEPALIVE_INTERVAL)
        mqttc.on_connect = on_connect
        mqttc.on_subscribe = on_subscribe
        mqttc.loop_start()
        publish_message(topics.CONNECT_REMOTE_REQUEST, None)
        return "Sent request to server to find remote.", 200
    except socket.timeout or Exception as e:
        print(e)
        return "Cannot find the remote client. Please make sure remote client is running on the same network.", 400
    
@app.route('/save-remote', methods=["POST"])
def save_remote_post():
    try:
        remote_name = request.json.get("remote_name", "")
        session["remote_name"] = remote_name
        return redirect(url_for('index'))
    except socket.timeout or Exception as e:
        return redirect(url_for('find_remote'))

@app.route('/', methods=["GET"])
@auth.remote_required
def index():
    data_manager.load_data()
    devices = data_manager.devices
    return render_template('index.html', devices=devices)

@app.route('/learn-command', methods=["POST"])
@auth.remote_required
def learn_command():
    try:
        publish_message(topics.LEARN_COMMAND_REQUEST, None)
        return "Sent request to server to learn IR command.", 200
    except ValueError as e:
        return str(e), 400
    except Exception as e:
        return "Something went wrong while learning command.", 500
    
@app.route('/add-device', methods=["POST"])
@auth.remote_required
def add_device():
    try:
        device_id = auth.generate_id()
        name = request.json.get("name")
        description = request.json.get("description")
        if name == "" or description == "":
            raise ValueError("Please enter all the values.")
        actions = []
        new_device = Device(device_id, name, description, actions)
        data_manager.devices.append(new_device)
        data_manager.save_data()
        return "Added device.", 200
    except ValueError as e:
        return str(e), 400
    except Exception as e:
        return "Something went wrong while adding device.", 500
    
@app.route('/add-action', methods=["POST"])
@auth.remote_required
def add_action():
    try:
        action_id = auth.generate_id()
        device_id = request.json.get("device_id")
        name = request.json.get("name")
        description = request.json.get("description")
        command = request.json.get("command")
        is_toggle = request.json.get("is_toggle")
        if device_id == "" or name == "" or description == "" or command == "" or not isinstance(is_toggle, bool):
            raise ValueError("Please enter all the values.")
        new_action = Action(action_id, device_id, name, description, command, is_toggle, 0 if is_toggle else -1)
        data_manager.add_action(new_action)
        data_manager.save_data()
        return "Added action to device.", 200
    except ValueError as e:
        return str(e), 400
    except Exception as e:
        return "Something went wrong while adding actions.", 500
    
@app.route('/send-command', methods=["POST"])
@auth.remote_required
def send_command():
    try:
        action_id = request.json.get("action_id", "")
        if action_id == "":
            raise ValueError("Please enter all the values.")
        action = data_manager.get_action_by_id(action_id)
        if action is None:
            raise ValueError("This commmand does not exist.")
        payload = { "command" : action.command }
        publish_message(topics.SEND_COMMAND_REQUEST, json.dumps(payload))
        return "Sent request to server to send IR command.", 200
    except ValueError as e:
        return str(e), 400
    except Exception as e:
        return "Something went wrong while sending command.", 500
    
@app.route('/disconnect', methods=["GET"])
def disconnect():
    if auth.connected:
        try:
            data_manager.save_data()
        except Exception as e:
            return str(e), 400
        finally:
            data_manager.devices = []
            auth.connected = False
            return redirect(url_for('find_remote')) 
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    socketio.run(app, debug=True, host=FLASK_HOSTNAME, port=FLASK_PORT)
