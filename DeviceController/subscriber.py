from enum import Enum
import time
import broadlink_client as broadlink_client
import paho.mqtt.client as mqtt
import json
import threading

# TODO: store packets
# TODO: configure network to connect to
# TODO: add error catching/throwing to handle error states
# TODO: error catching for network/json/state

class BroadlinkState(Enum):
	DISCOVER_BROADLINK = "DISCOVER_BROADLINK"
	DISCOVER_BROADLINK = "DISCOVER_BROADLINK"
	START_LEARNING = "START_LEARNING"
	STOP_LEARNING = "STOP_LEARNING"
	SEND_PACKET = "SEND_PACKET"
	
class Topic(Enum):
	BROADLINK = "broadlink"
	CAMERA = "camera"


TICK = 32.84
TIMEOUT = 30
IR_TOKEN = 0x26

def auto_int(x):
    return int(x, 0)


def to_microseconds(bytes):
    result = []
    #  print bytes[0] # 0x26 = 38for IR
    index = 4
    while index < len(bytes):
        chunk = bytes[index]
        index += 1
        if chunk == 0:
            chunk = bytes[index]
            chunk = 256 * chunk + bytes[index + 1]
            index += 2
        result.append(int(round(chunk * TICK)))
        if chunk == 0x0d05:
            break
    return result


def durations_to_broadlink(durations):
    result = bytearray()
    result.append(IR_TOKEN)
    result.append(0)
    result.append(len(durations) % 256)
    result.append(len(durations) / 256)
    for dur in durations:
        num = int(round(dur / TICK))
        if num > 255:
            result.append(0)
            result.append(num / 256)
        result.append(num % 256)
    return result


def format_durations(data):
    result = ''
    for i in range(0, len(data)):
        if len(result) > 0:
            result += ' '
        result += ('+' if i % 2 == 0 else '-') + str(data[i])
    return result


def parse_durations(str):
    result = []
    for s in str.split():
        result.append(abs(int(s)))
    return result

   
def process_broadlink(raw_payload):
	payload = json.loads(raw_payload)
	state = payload['state']
	if state is BroadlinkState.DISCOVER_BROADLINK:
		connect_broadlink()
	elif state is BroadlinkState.STOP_LEARNING:
		print("Stop learning IR signals")
	elif state is BroadlinkState.SEND_PACKET:
		print("Send IR signal")
	else: 
		print("Invalid state")
  
def process_message(msg):
	if msg.topic is Topic.BROADLINK:
		process_broadlink(msg)
	elif msg.topic is Topic.CAMERA:
		print("Process packet as a Camera message")
	else: 
		print("Invalid topic")


def on_connect(mqttc, obj, flags, reason_code, properties):
	print("Reason code: " + str(reason_code))

def on_message(mqttc, obj, msg):
	print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
	payload = json.loads(msg.payload.decode('utf-8'))
	state = payload['state']
	if state is State.START_LEARNING:
		print("Start learning IR signals")
	elif state is State.STOP_LEARNING:
		print("Stop learning IR signals")
	elif state is State.SEND_PACKET:
		print("Send IR signal to device")
	else: 
		print("Invalid state")

def find_devices():
	print("Finding devices")
	devices = broadlink.discover(timeout=5)
	if devices:
		device = devices[0]
		device.auth()
		print("Found device and authenticated")
	else:
		print("No devices found")
	
def on_subscribe(mqttc, obj, mid, reason_code_list, properties):
	print("Subscribed: " + str(mid) + " " + str(reason_code_list))

def on_log(mqttc, obj, level, string):
	print(string)

def configure_broadlink():
	print("Setting up Broadlink...")
	broadlink_client.setup('some phone', 'password', 3)
	print("Set up complete!")

def connect_broadlink():
	print("Discovering devices...")
	devices = []
	while not devices:
		devices = broadlink_client.discover()
	device = devices[0]
	print("Found a device!")
	device.auth()
	return device
 
def discover_signal(device: broadlink_client.Device):
	start = time.time()
	device.enter_learning()
	while time.time() - start < TIMEOUT:
		try:   
			packet = device.check_data()
			print(packet.hex())
			send_signal(device, packet)
			# return packet
		except (broadlink_client.exceptions.ReadError, broadlink_client.exceptions.StorageError):
			continue
		else:
			break
	else:
		print("No data received...")
		exit(1)

def send_signal(device: broadlink_client.Device, packet):
	device.send_data(packet)
	discover_signal(device)

		


print("Subscribing to topic...")
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_log = on_log
mqttc.connect("mqtt.eclipseprojects.io", 1883, 60)
mqttc.subscribe("$SYS/#")

device_thread = threading.Thread(target=find_devices)
device_thread.start()

mqttc.loop_start
mqttc.loop_forever()

configure_broadlink()
device: broadlink_client.Device = connect_broadlink()
packet = discover_signal(device)
device.send_data(packet)