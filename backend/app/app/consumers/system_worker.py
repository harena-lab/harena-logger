from raven import Client
from app.core.config import settings
from app.core.kafka_app import faust_app as app, topic, Greeting
from app.models import KafkaMessageDocument, KafkaMessageRecord
from mongoengine import connect

client_sentry = Client(settings.SENTRY_DSN)

connect(db='logger-dev', host='mongo', port=27017, username='logger', password='harena')

kafka_messages_topic = app.topic('system_message', value_type=KafkaMessageRecord)

boot_topic = app.topic('boot', value_type=Greeting)

@app.agent(kafka_messages_topic)
async def sendKafkaMessageToMongoDB(kafka_messages):
    async for kafka_msg in kafka_messages:
        input = KafkaMessageDocument(version=kafka_msg.version, topic=kafka_msg.topic,
                                     message_class=kafka_msg.message_class, message_subclass=kafka_msg.message_subclass,
                                     payload_metadata=kafka_msg.payload_metadata, payload_body=kafka_msg.payload_body,
                                     timestamp=kafka_msg.timestamp, origin_ip=kafka_msg.origin_ip)
        input.save()
        print('Saved case: ' + str(input.message_class) + ' event ' + input.message_subclass + ' to MongoDB')

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