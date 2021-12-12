from elasticsearch import Elasticsearch
import os

ElasticSearchConnection = Elasticsearch(
    hosts=[{"host": os.getenv("ELASTICSEARCH_SERVER"), "port": os.getenv("ELASTICSEARCH_PORT")}],
    http_auth=[os.getenv("ELASTICSEARCH_USERNAME"), os.getenv("ELASTICSEARCH_PASSWORD")],
)