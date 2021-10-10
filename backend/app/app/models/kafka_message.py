from mongoengine import connect, Document, BooleanField, ObjectIdField, StringField, IntField
from faust import Record

class KafkaMessageDocument(Document):
    _id = ObjectIdField()
    case = IntField()
    payload = StringField()
    origin_ip = StringField()
    event = StringField()


class KafkaMessageRecord(Record, serializer='json'):
    case: int
    payload: str
    origin_ip: str
    event: str

