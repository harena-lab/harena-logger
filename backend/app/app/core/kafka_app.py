import faust
import kafka
import json

class Greeting(faust.Record, serializer='json'):
    from_name: str
    to_name: str

faust_app = faust.App(
    'harena-logger',
    broker='kafka://brokerkafka:9092',
    value_serializer='raw',
)
topic = faust_app.topic('greetings2', value_type=Greeting)

producer = kafka.KafkaProducer(bootstrap_servers=['brokerkafka:9092'],
                               value_serializer=lambda x:
                               x.dumps())

def synchronousSend(topicname, data):
    future = producer.send(topicname, value=data)
    record_metadata = future.get(timeout=10)