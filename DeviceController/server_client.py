from .states import States as states
import paho.mqtt.client as mqtt
import json

class ServerClient:
	mqttc: mqtt.Client

	def __init__(self):
		self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

	def initialise_connection(self):
		self.mqttc.on_message = self.on_message
		self.mqttc.on_connect = self.on_connect
		self.mqttc.on_subscribe = self.on_subscribe
		self.mqttc.on_log = self.on_log
		self.mqttc.connect("mqtt.eclipseprojects.io", 1883, 60)
		self.mqttc.subscribe("$SYS/#")
		self.mqttc.loop_forever()

	def on_connect(mqttc, obj, flags, reason_code, properties):
		print("Reason code: " + str(reason_code))

	def on_message(mqttc, obj, msg):
		print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

	def on_subscribe(mqttc, obj, mid, reason_code_list, properties):
		print("Subscribed: " + str(mid) + " " + str(reason_code_list))

	def on_log(mqttc, obj, level, string):
		print(string)