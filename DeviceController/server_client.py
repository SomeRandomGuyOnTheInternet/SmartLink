import topics
import json
import broadlink
import paho.mqtt.client as mqtt
from remote_client import RemoteClient
from remote_exception import RemoteException

BROKER_ADDRESS = "localhost"

class ServerClient:
	mqttc: mqtt.Client
	client_id: str
	hostname: str
	port: str
	network_ssid: str
	network_password: str
	network_security: str
	remote_client: RemoteClient
	success_response = {"response": "success"}
	error_response = {"response": "error", "status": "", "message": ""}

	def __init__(self, client_id, hostname, port, remote_client):
		self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
		self.client_id = client_id
		self.hostname = hostname
		self.port = port
		self.remote_client = remote_client

	def initialise(self):
		self.mqttc.on_connect = self.on_connect
		self.mqttc.on_subscribe = self.on_subscribe
		self.mqttc.on_message = self.on_message
		self.mqttc.on_log = self.on_log
		self.mqttc.connect(self.hostname, int(self.port), 60)
		self.mqttc.subscribe(topics.CONNECT_REMOTE_REQUEST)
		self.mqttc.subscribe(topics.LEARN_COMMAND_REQUEST)
		self.mqttc.subscribe(topics.SEND_COMMAND_REQUEST)
		self.mqttc.message_callback_add(topics.CONNECT_REMOTE_REQUEST, self.on_message_connect_remote)
		self.mqttc.message_callback_add(topics.LEARN_COMMAND_REQUEST, self.on_message_learn_command)
		self.mqttc.message_callback_add(topics.SEND_COMMAND_REQUEST, self.on_message_send_command)
		self.mqttc.loop_forever()
			

	def on_connect(self, mqttc, obj, flags, reason_code, properties):
		print("Reason code: " + str(reason_code))
		
	def on_message(self, mqttc, obj, msg):
		print("recieved message")

	def on_message_connect_remote(self, mqttc, obj, msg):
		try:
			remote: broadlink.Device = self.remote_client.connect_to_remote()
			payload = self.success_response
			payload["device_name"] = remote.name			
		except RemoteException as e:
			payload = self.error_response
			payload["status"] = e.status
			payload["message"] = e.message
		except (UnboundLocalError, json.decoder.JSONDecodeError) as e:
			payload = self.error_response
			payload["status"] = "IncorrectPayloadFormat"
			payload["message"] = "Payload is incorrectly formatted"
		finally:
			payload = json.dumps(payload)
			mqttc.publish(topics.CONNECT_REMOTE_RESPONSE, payload, qos=1)

	def on_message_learn_command(self, mqttc, obj, msg):
		try:
			payload = json.loads(msg.payload)
			command = self.remote_client.discover_command()
			payload = self.success_response
			payload["command"] = command			
		except RemoteException as e:
			payload = self.error_response
			payload["status"] = e.status
			payload["message"] = e.message
		except (UnboundLocalError, json.decoder.JSONDecodeError) as e:
			payload = self.error_response
			payload["status"] = "IncorrectPayloadFormat"
			payload["message"] = "Payload is incorrectly formatted"
		finally:
			payload = json.dumps(payload)
			mqttc.publish(topics.LEARN_COMMAND_RESPONSE, payload, qos=1)

	def on_message_send_command(self, mqttc, obj, msg):
		try:
			payload = json.loads(msg.payload)
			self.remote_client.send_command(payload["command"])
			payload = self.success_response		
		except RemoteException as e:
			payload = self.error_response
			payload["status"] = e.status
			payload["message"] = e.message
		except (UnboundLocalError, json.decoder.JSONDecodeError) as e:
			payload = self.error_response
			payload["status"] = "IncorrectPayloadFormat"
			payload["message"] = "Payload is incorrectly formatted"
		finally:
			payload = json.dumps(payload)
			mqttc.publish(topics.SEND_COMMAND_RESPONSE, payload, qos=1)

	def on_subscribe(self, mqttc, obj, mid, reason_code_list, properties):
		print("Subscribed: " + str(mid) + " " + str(reason_code_list))

	def on_log(self, mqttc, obj, level, string):
		print(string)
