import os
import json
import paho.mqtt.client as paho
import random
import pymongo
import time
import threading
import logging
import coloredlogs

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from config import Config
from flask_cors import CORS, cross_origin
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError

# To do: Logging not appearing in Docker logs
LOGGER = logging.getLogger(Config.LOGGING_NAME)

class KafkaMongodbAppender (threading.Thread):

   def __init__(self, mongodb_server_url, mongodb_database, mongodb_collection, kafka_consumer, topic, delay):
      threading.Thread.__init__(self)
      self.mongodb_server_url = mongodb_server_url
      self.mongodb_database = mongodb_database
      self.mongodb_collection = mongodb_collection
      self.kafka_consumer = kafka_consumer
      self.topic = topic
      self.delay = delay
      LOGGER.debug(mongodb_server_url)

   def run(self):

      LOGGER.info("Starting KafkaMongodbAppender")

      while True:
         
         # Opening and closing the connection during streamming checking. 
         # Adopting this since some memory problems appeared after long term one connection management
         mongodb_client = pymongo.MongoClient(self.mongodb_server_url) 
         mongodb_db = mongodb_client[self.mongodb_database]
         mongodb_collection = mongodb_db[self.mongodb_collection]

         print("Checking for newly streamed messages during at least {} seconds...".format(self.delay))
         try:
            for message in self.kafka_consumer:
               #print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))
                  print("Found {} events inside a message ".format(len(message.value['harena-log-stream'])))
                  for event in message.value['harena-log-stream']:
                     mongodb_collection.insert_one(event)
         except:
                print("Object is not a JSON or does not have an 'harena-log-stream' array")


         print("Waiting time ({} seconds) for new messages ended.".format(self.delay)) 
         mongodb_client.close()
         time.sleep(self.delay)


class IndexResource(Resource):

    def __init__(self, kafka_producer):
      self.kafka_producer=kafka_producer
      
      LOGGER.debug("IndexResource initialized")


    def get(self):
      message = {"message": "Welcome to the Harena Logger module",
                 "kafka_bootstrap_connected" : self.kafka_producer.bootstrap_connected()
      }
      return message


class HarenaMessageResource(Resource):

    def __init__(self, kafka_producer, target_topic):
        self.kafka_producer = kafka_producer
        self.target_topic=target_topic

        

    @cross_origin(origin='*')
    def post(self):

        try:
           # To do: properly evaluate message body parsing
           message = request.get_json()
           message['server_timestamp'] = "{}".format(int(round(time.time() * 1000)))

           # Asynchronous by default
           future = self.kafka_producer.send(self.target_topic, json.dumps(message).encode('utf-8'))

           # Block for 'synchronous' sends
           record_metadata = future.get(timeout=10)
        except KafkaError:
           # Decide what to do if produce request failed...
           log.exception()
        except:
           print("could not validate the json")

        # Successful result returns assigned partition and offset
        # print(future)

        data = {"message":'Message published successfully'}

        return jsonify(data)        


    @cross_origin(origin='*')
    def get(self):
        message = {"message": "message streaming is up",
                  "kafka_bootstrap_connected" : self.kafka_producer.bootstrap_connected()
        
        }
        return message


if __name__ == '__main__':


    kafka_producer = None
    kafka_consumer = None


    while True:
        try:
            kafka_producer = KafkaProducer(bootstrap_servers=Config.HARENA_LOGGER_KAFKA_BROKERS)
            
            kafka_consumer = KafkaConsumer(Config.HARENA_LOGGER_KAFKA_TOPIC, group_id='harena-logger-consumer', 
                                                                             bootstrap_servers=Config.HARENA_LOGGER_KAFKA_BROKERS,
                                                                             value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                                                             consumer_timeout_ms=Config.HARENA_LOGGER_INTERVAL_S*1000)
            break
        except:    
            pass

        print("Could not exchange metadata with Kafka bootstrap servers for the first time. Retrying...")
        time.sleep(1)




    consumer_thread = KafkaMongodbAppender(mongodb_server_url=Config.HARENA_LOGGER_MONGODB_URL,
                                           mongodb_database=Config.HARENA_LOGGER_MONGODB_DB, 
                                           mongodb_collection=Config.HARENA_LOGGER_MONGODB_COLLECTION,
                                           kafka_consumer=kafka_consumer,
                                           topic=Config.HARENA_LOGGER_KAFKA_TOPIC, 
                                           delay=Config.HARENA_LOGGER_INTERVAL_S)
    consumer_thread.start()


    # Web Service for appending
    web_app = Flask(__name__)
    web_app.config.from_object(Config)
    CORS(web_app)
    api = Api(web_app)
    api.add_resource(IndexResource,         '/',              resource_class_args=[kafka_producer])
    api.add_resource(HarenaMessageResource, '/api/v1/message',resource_class_args=[kafka_producer, Config.HARENA_LOGGER_KAFKA_TOPIC])
    web_app.run(host=web_app.config['HARENA_LOGGER_FLASK_HOST'],
                port=web_app.config['HARENA_LOGGER_FLASK_PORT'],
                debug=web_app.config['HARENA_LOGGER_FLASK_DEBUG'])
