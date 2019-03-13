from flask import Flask, request
import paho.mqtt.client as paho
import random

app = Flask(__name__)

broker_host    = "broker"
broker_port      = 1883 

broker = paho.Client("publisher{0}".format(random.randint(0,99999999)) )
broker.connect(broker_host,broker_port)

@app.route('/')
def index():
    return 'Harena Logger Relayer'

@app.route('/publish', methods=['POST'])
def publish():

	# payload = request.args.get('payload', '')

	message = request.get_json()
	print(message)
	topic   = message['topic']
	payload = message['payload']


	broker.publish(topic,payload) 

	return 'Message published successfully'


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=8080, debug=True)