from flask import Flask, request
from flask_restful import Resource, Api
import paho.mqtt.client as paho
import random



broker_host    = "broker"
broker_port    = 1883

broker = paho.Client("publisher{0}".format(random.randint(0,99999999)) )
broker.connect(broker_host,broker_port)  


@app.route('/')
def index():
    return 'Harena Logger Relayer'

class HarenaMessageResource(Resource):

    def post(self):
    	message = request.get_json()
    	print(message)
    	topic   = message['topic']
    	payload = message['payload']

    	broker.publish(topic,payload)

    	return 'Message published successfully'   
    

if __name__ == '__main__':
  
  web_app = Flask(__name__)

  api     = Api(web_app)
  
  api.add_resource(HarenaMessageResource, '/message')
  
	web_app.run(host="0.0.0.0", port=8080)
