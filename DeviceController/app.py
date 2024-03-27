from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt

app = Flask(name)

# MQTT Configuration
MQTT_BROKER_URL = "localhost"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "home/switch"

# Initialize MQTT Client
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
print("Connecting to MQTT broker....")
mqtt_client.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT, 60)
print("Connected to MQTT broker.")
mqtt_client.loop_start()

# Route for serving the HTML
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling the switch toggle
@app.route('/toggle_switch', methods=['POST'])
def toggle_switch():
    state = request.json.get('state', '')
    # Publish the switch state to MQTT
    print("Publishing state to MQTT topic")
    mqtt_client.publish(MQTT_TOPIC, state)
    return jsonify({"success": True, "state": state})
    

if name == 'main':
 app.run(debug=True, host='0.0.0.0',port=5000)
