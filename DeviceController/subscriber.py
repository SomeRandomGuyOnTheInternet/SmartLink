from enum import Enum
import broadlink as broadlink
import paho.mqtt.client as mqtt
import json

class State(Enum):
    START_LEARNING = "start_learning"
    STOP_LEARNING = "end_learning"
    SEND_PACKET = "send_packet"

def on_connect(mqttc, obj, flags, reason_code, properties):
    print("Reason code: " + str(reason_code))


def on_message(mqttc, obj, msg):
	print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
	payload = json.loads(msg.payload)
	state = payload['state']
	if state is State.START_LEARNING:
		print("Start learning IR signals")
	elif state is State.STOP_LEARNING:
		print("Stop learning IR signals")
	elif state is State.SEND_PACKET:
		print("Send IR signal to device")
	else: 
		print("Invalid state")


def on_subscribe(mqttc, obj, mid, reason_code_list, properties):
	print("Subscribed: " + str(mid) + " " + str(reason_code_list))


def on_log(mqttc, obj, level, string):
    print(string)

print("Subscribing to topic...")
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
# mqttc.on_log = on_log
mqttc.connect("mqtt.eclipseprojects.io", 1883, 60)
mqttc.subscribe("$SYS/#")
mqttc.loop_forever()

print("Discovering devices...")
devices = []
while not devices:
    devices = broadlink.discover()
device = devices[0]
print("Found a device!")
device.auth()
