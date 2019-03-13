from flask import Flask, request
from flask_restful import Resource, Api
import paho.mqtt.client as paho
import random

app = Flask(__name__)
api = Api(app)

broker_host    = "broker"
broker_port    = 1883

broker = paho.Client("publisher{0}".format(random.randint(0,99999999)) )
broker.connect(broker_host,broker_port)

@app.route('/')
def index():
    return 'Harena Logger Relayer'

class Publisher(Resource):

	# payload = request.args.get('payload', '')
    def post(self):
    	message = request.get_json()
    	print(message)
    	topic   = message['topic']
    	payload = message['payload']

    	broker.publish(topic,payload)

    	return 'Message published successfully'

api.add_resource(Publisher, '/publish')

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=8080, debug=True)
