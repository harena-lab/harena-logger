from raven import Client
from app.core.config import settings
from app.core.kafka_app import faust_app as app, topic, Greeting
from app.models import UserActionDocument, KafkaMessageRecord
from mongoengine import connect
from fastapi import Depends
from app.api import deps
client_sentry = Client(settings.SENTRY_DSN)

kafka_messages_topic = app.topic('user_action', value_type=KafkaMessageRecord)

@app.agent(kafka_messages_topic)
async def sendKafkaMessageToMongoDB(kafka_messages, connect: connect = Depends(deps.get_mongo_db())):
    async for kafka_msg in kafka_messages:
        input = UserActionDocument(version=kafka_msg.version, topic=kafka_msg.topic,
                                     message_class=kafka_msg.message_class, message_subclass=kafka_msg.message_subclass,
                                     payload_metadata=kafka_msg.payload_metadata, payload_body=kafka_msg.payload_body,
                                     timestamp=kafka_msg.timestamp, origin_ip=kafka_msg.origin_ip)

        input.save()
        print('Saved case: ' + str(input.message_class) + ' event ' + input.message_subclass + ' to MongoDB')


@app.timer(interval=120.0)
async def example_sender(faust_app, connect: connect = Depends(deps.get_mongo_db())):
    await topic.send(
        value=Greeting(from_name='Action Worker', to_name='Kafka').dumps()
    )