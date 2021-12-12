from raven import Client
from app.core.config import settings
from app.core.kafka_app import faust_app as app, topic, Greeting
from app.models import SystemMessageDocument, KafkaMessageRecord
from app.db.mongo import connect
from app.db.elasticsearch import ElasticSearchConnection
from fastapi import Depends
from app.api import deps

client_sentry = Client(settings.SENTRY_DSN)

kafka_messages_topic = app.topic('system_message', value_type=KafkaMessageRecord)

boot_topic = app.topic('boot', value_type=Greeting)

@app.agent(kafka_messages_topic)
async def sendKafkaMessageToMongoDB(kafka_messages):
    async for kafka_msg in kafka_messages:
        ElasticSearchConnection.index(index='system-message', document=kafka_msg.dumps())

        print('Saved case: ' + str(kafka_msg.message_class) + ' event ' + kafka_msg.message_subclass + ' to ElasticSearch')

@app.agent(topic)
async def hello(greetings):
    async for greeting in greetings:
        print(f'Hello from {greeting.from_name} to {greeting.to_name}')

@app.agent(boot_topic)
async def boot(greetings):
    async for greeting in greetings:
        print(f'Boot message from {greeting.from_name} to {greeting.to_name}')

@app.timer(interval=120.0)
async def example_sender(faust_app):
    await topic.send(
        value=Greeting(from_name='System Worker', to_name='Kafka').dumps()
    )