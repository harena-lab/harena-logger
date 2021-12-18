from raven import Client
from app.core.config import settings
from app.core.kafka_app import faust_app as app, topic, Greeting
from app.models import UserActionDocument, KafkaMessageRecord
from app.db.elasticsearch import ElasticSearchConnection
from fastapi import Depends
from app.api import deps
#Bibliotecas adicionadas
import json
from datetime import datetime, time

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
    response = ElasticSearchConnection.search(index='user-action', body=search_param)
    for doc in response['hits']['hits']:
        doc['_source']['payload_body'] = json.loads(doc['_source']['payload_body'])
        ElasticSearchConnection.index(index='case-summary', document=json.dumps(doc['_source']))

# @app.timer(interval=30.0)
# async def delete_indices(faust_app):
#     print("apagando")
#     indices = ['report']
#     ElasticSearchConnection.delete_by_query(index=indices, body={"query": {"match_all": {}}})


@app.timer(interval=180.0)
async def create_report(faust_app):
    fmt = '%Y-%m-%dT%H:%M:%S.%fZ'
    search_param = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"message_subclass": "case_summary"}},
                ],
                "filter": [
                    {"range": {"timestamp": {"gte": "now-3m/m"}}}
                ]
            }
        }
    }
    response = ElasticSearchConnection.search(index='user-action', body=search_param)
    for doc in response['hits']['hits']:
        summary = json.loads(doc['_source']['payload_body'])
        session_id = doc['_source']['topic'].split('/')[2]
        case_id = summary['caseId']
        log_time = doc['_source']['timestamp']
        dummy = {"session_id": session_id, "case_id": case_id, "log_time": log_time}

        for knot_number in range(len(summary["knotTrack"])):
            if knot_number != len(summary["knotTrack"]) - 1:
                knot = summary["knotTrack"][knot_number]
                knot_id = knot["knotid"]
                time_start = knot["timeStart"]
                if knot_number+1 == len(summary["knotTrack"]) - 1:
                    time_end = summary["knotTrack"][knot_number+1]["timeCompleted"]
                else:
                    time_end = summary["knotTrack"][knot_number+1]["timeStart"]
                duration_mins = int(round((datetime.strptime(time_end, fmt) - datetime.strptime(time_start, fmt)).total_seconds()))
                knot_var_name = knot_id+".hypothesis"
                if knot_var_name in summary["variables"].keys():
                    knot_var = summary["variables"][knot_var_name]
                else:
                    knot_var = ""
                dummy["knot_id"] = knot_id
                dummy["time_start"] = time_start
                dummy["time_end"] = time_end
                dummy["duration_mins"] = duration_mins
                dummy["knot_var"] = knot_var
                print(dummy)
                ElasticSearchConnection.index(index='report', document=json.dumps(dummy))
