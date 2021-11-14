from mongoengine import connect, Document, BooleanField, ObjectIdField, StringField, IntField, DateTimeField
from faust import Record
from datetime import  datetime

class KafkaMessageDocument(Document):
    _id = ObjectIdField()
    version: StringField()
    topic: StringField()
    payload_metadata: StringField()
    payload_body: StringField()
    timestamp: DateTimeField()
    origin_ip: StringField()

class KafkaMessageRecord(Record, serializer='json'):
    version: Optional[str] = None
    topic: Optional[str] = None
    payload_metadata: Optional[str] = None
    payload_body: Optional[str] = None
    timestamp: Optional[datetime] = None
    origin_ip: Optional[str] = None

