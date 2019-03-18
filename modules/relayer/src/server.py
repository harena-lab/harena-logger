import os
import json
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import paho.mqtt.client as paho
import random
import pymongo
import time


class IndexResource(Resource):

    def __init__(self,broker,mongodb_client):
      self.broker = broker

    def get(self):
      message = {"message": "Welcome to the Harena Logger module",
                 "broker_status" : broker.__repr__(),
                 "database_status":mongodb_client.server_info()

      }
      return message



class HarenaMessageResource(Resource):

    def __init__(self, broker, mongodb_collection):
      self.broker = broker
      self.mongodb_collection = mongodb_collection

    def post(self):
      message = request.get_json()
      print(json.dumps(message))
      topic   = message['topic']
      payload = message['payload']

      message['timestamp'] = "{}".format(int(round(time.time() * 1000)))

      broker_publishing_flag = self.broker.publish(topic,json.dumps(payload))
      mongodb_insertion_flag = self.mongodb_collection.insert(message)

      return 'Message published successfully',201

    def get(self):
      docs = self.mongodb_collection.find().sort([("timestamp", pymongo.DESCENDING)])

      items = []

      for doc in docs:
        doc['_id'] = str(doc['_id'])
        items.append(doc)

      return jsonify({'execution_stream':items})

    def delete(self):
      self.mongodb_collection.delete_many({})

      return 'Messages in the execution stream deleted successfully'




if __name__ == '__main__':
  
      web_app = Flask(__name__)
      api     = Api(web_app)

      config     = {}
      config['broker_host']        = os.environ.get('HARENA_LOGGER_BROKER_HOST', 'localhost')
      config['broker_port']        = int(os.environ.get('HARENA_LOGGER_BROKER_PORT', 1883))

      config['flask_host']         = os.environ.get('HARENA_LOGGER_FLASK_HOST',  '0.0.0.0')
      config['flask_port']         = int(os.environ.get('HARENA_LOGGER_FLASK_PORT',  5000))
      config['flask_debug']        = bool(os.environ.get('HARENA_LOGGER_FLASK_DEBUG', False))

      config['mongodb_host']       = os.environ.get('HARENA_LOGGER_MONGODB_HOST',       'localhost')
      config['mongodb_port']       = int(os.environ.get('HARENA_LOGGER_MONGODB_PORT',       27017))
      config['mongodb_db']         = os.environ.get('HARENA_LOGGER_MONGODB_DB',         'harena_logger')
      config['mongodb_collection'] = os.environ.get('HARENA_LOGGER_MONGODB_COLLECTION', 'executions')

      mongodb_client     = pymongo.MongoClient("mongodb://{0}:{1}/".format(config['mongodb_host'],config['mongodb_port']))
      mongodb_db         = mongodb_client[config['mongodb_db']]
      mongodb_collection = mongodb_db[    config['mongodb_collection']]

      broker = paho.Client("publisher{0}".format(random.randint(0,99999999)) )
      broker.connect(config['broker_host'],config['broker_port'])  
      broker.reconnect_delay_set(min_delay=1, max_delay=20)

      api.add_resource(IndexResource,         '/',       resource_class_args=[broker,mongodb_client])
      api.add_resource(HarenaMessageResource, '/message',resource_class_args=[broker,mongodb_collection])

      web_app.run(host=config['flask_host'], port=config['flask_port'],debug=config['flask_debug'])
