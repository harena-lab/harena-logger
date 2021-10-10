from raven import Client
from app.core.config import settings
from app.core.kafka_app import faust_app as app, topic, Greeting
from app.models import KafkaMessageDocument, KafkaMessageRecord
from mongoengine import connect

client_sentry = Client(settings.SENTRY_DSN)

connect(db='logger-dev', host='mongo', port=27017, username='logger', password='harena')

kafka_messages_topic = app.topic('log_raw_default', value_type=KafkaMessageRecord)

@app.agent(kafka_messages_topic)
async def sendKafkaMessageToMongoDB(kafka_messages):
    async for kafka_msg in kafka_messages:
        input = KafkaMessageDocument(case=kafka_msg.case, payload=kafka_msg.payload, event=kafka_msg.event, origin_ip=kafka_msg.origin_ip)
        input.save()
        print('Saved case: ' + str(input.case) + ' event ' + input.event + 'to MongoDB')

@app.agent(topic)
async def hello(greetings):
    async for greeting in greetings:
        print(f'Hello from {greeting.from_name} to {greeting.to_name}')

@app.timer(interval=10.0)
async def example_sender(faust_app):
    await topic.send(
        value=Greeting(from_name='Faust', to_name='you').dumps()
    )