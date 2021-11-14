from mongoengine import connect, Document, BooleanField, ObjectIdField, StringField, IntField, DateTimeField
from faust import Record
from datetime import  datetime

class KafkaMessageDocument(Document):
    _id = ObjectIdField()
    version: StringField()
    topic: StringField()
    payload_metadata: StringField()
    payload_body: StringField()
    message_class: StringField()
    message_subclass: StringField()
    timestamp: DateTimeField()
    origin_ip: StringField()

class KafkaMessageRecord(Record, serializer='json'):
    version: str
    topic: str
    message_class: str
    message_subclass: str
    payload_metadata: str
    payload_body: str
    timestamp: datetime
    origin_ip: str

