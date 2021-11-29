import faust
import kafka
import json

import os


class Greeting(faust.Record, serializer='json'):
    from_name: str
    to_name: str

APP_KAFKA_SERVER_PORT=os.getenv("APP_KAFKA_SERVER_PORT", "brokerkafka")

faust_app = faust.App(
    'harena-logger',
    broker=f"kafka://{APP_KAFKA_SERVER_PORT}",
    value_serializer='raw',
)
topic = faust_app.topic('greetings2', value_type=Greeting)

producer = kafka.KafkaProducer(bootstrap_servers=[APP_KAFKA_SERVER_PORT],
                               value_serializer=lambda x: x.dumps())

def synchronousSend(topicname, data):
    future = producer.send(topicname, value=data)
    record_metadata = future.get(timeout=10)