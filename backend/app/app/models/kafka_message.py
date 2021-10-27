from mongoengine import connect, Document, BooleanField, ObjectIdField, StringField, IntField, DateTimeField
from faust import Record
from datetime import  datetime

class KafkaMessageDocument(Document):
    _id = ObjectIdField()
    session_id = IntField()
    user_id = IntField()
    case_id = IntField()
    knot_id = IntField()
    timestamp = DateTimeField()
    hipothesis = StringField()
    origin_ip = StringField()

class KafkaMessageRecord(Record, serializer='json'):
    origin_ip: str
    session_id: int
    user_id: int
    case_id: int
    knot_id: int
    timestamp: datetime
    hipothesis: str

