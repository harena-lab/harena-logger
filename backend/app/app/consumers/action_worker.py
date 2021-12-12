from raven import Client
from app.core.config import settings
from app.core.kafka_app import faust_app as app, topic, Greeting
from app.models import UserActionDocument, KafkaMessageRecord
from app.db.elasticsearch import ElasticSearchConnection
from fastapi import Depends
from app.api import deps
client_sentry = Client(settings.SENTRY_DSN)

kafka_messages_topic = app.topic('user_action', value_type=KafkaMessageRecord)

@app.agent(kafka_messages_topic)
async def sendKafkaMessageToMongoDB(kafka_messages):
    async for kafka_msg in kafka_messages:
        ElasticSearchConnection.index(index='user-action', document=kafka_msg.dumps())

        print('Saved case: ' + str(kafka_msg.message_class) + ' event ' + kafka_msg.message_subclass + ' to ElasticSearch')


@app.timer(interval=120.0)
async def example_sender(faust_app):
    await topic.send(
        value=Greeting(from_name='Action Worker', to_name='Kafka').dumps()
    )