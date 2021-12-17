from raven import Client
from app.core.config import settings
from app.core.kafka_app import faust_app as app, topic, Greeting
from app.models import UserActionDocument, KafkaMessageRecord
from app.db.elasticsearch import ElasticSearchConnection
from fastapi import Depends
from app.api import deps
import json

client_sentry = Client(settings.SENTRY_DSN)

kafka_messages_topic = app.topic('user_action', value_type=KafkaMessageRecord)

@app.agent(kafka_messages_topic)
async def sendKafkaMessageToMongoDB(kafka_messages):
    async for kafka_msg in kafka_messages:
        print("ASDIHJGASOIDUSA")
        print(type(kafka_msg))
        ElasticSearchConnection.index(index='user-action', document=kafka_msg.dumps())

        print('Saved case: ' + str(kafka_msg.message_class) + ' event ' + kafka_msg.message_subclass + ' to ElasticSearch')


@app.timer(interval=120.0)
async def example_sender(faust_app):
    await topic.send(
        value=Greeting(from_name='Action Worker', to_name='Kafka').dumps()
    )

@app.timer(interval=300.0)
async def treat_summary(faust_app):
    search_param = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"message_subclass": "case_summary"}},
                ],
                "filter": [
                    {"range": {"timestamp": {"gte": "now-5m/m"}}}
                ]
            }
        }
    }
    print("Realizando busca")
    response = ElasticSearchConnection.search(index='user-action', body=search_param)
    for doc in response['hits']['hits']:
        print(type(doc))
        doc['_source']['payload_body'] = json.loads(doc['_source']['payload_body'])
        print(doc)
        ElasticSearchConnection.index(index='case-summary', document=json.dumps(doc['_source']))

# @app.timer(interval=30.0)
# async def delete_indices(faust_app):
#     indices = ['case-summary', 'user-action', 'system-message']
#     ElasticSearchConnection.delete_by_query(index=indices, body={"query": {"match_all": {}}})
