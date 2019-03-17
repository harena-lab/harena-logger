import os
import json
from flask import Flask, request
from flask_restful import Resource, Api
import paho.mqtt.client as paho
import random






class IndexResource(Resource):

    def __init__(self,broker):
      print(broker)
      self.broker = broker

    def get(self):
      message = {"message": "Harena Logger Relayer",
                 "broker" : broker.__repr__()
      }
      return message



class HarenaMessageResource(Resource):

    def __init__(self,broker):
      print(broker)
      self.broker = broker


    def post(self):
    	message = request.get_json()
    	print(json.dumps(message))
    	topic   = message['topic']
    	payload = message['payload']

    	self.broker.publish(topic,payload)

    	return 'Message published successfully'   
    

if __name__ == '__main__':
  
      web_app = Flask(__name__)
      api     = Api(web_app)

      config     = {}
      config['broker_host'] = os.environ.get('HARENA_LOGGER_BROKER_HOST', 'localhost')
      config['broker_port'] = os.environ.get('HARENA_LOGGER_BROKER_PORT', 1883)
      config['flask_host']  = os.environ.get('HARENA_LOGGER_FLASK_HOST',  '0.0.0.0')
      config['flask_port']  = os.environ.get('HARENA_LOGGER_FLASK_PORT',  5000)
      config['flask_debug'] = bool(os.environ.get('HARENA_LOGGER_FLASK_DEBUG', 'False'))


      broker = paho.Client("publisher{0}".format(random.randint(0,99999999)) )
      broker.connect(config['broker_host'],config['broker_port'])  

      api.add_resource(IndexResource,         '/',       resource_class_args={'broker': broker})
      api.add_resource(HarenaMessageResource, '/message',resource_class_args={'broker': broker})

      web_app.run(host=config['flask_host'], port=config['flask_port'],debug=config['flask_debug'])
