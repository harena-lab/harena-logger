from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr


# Shared properties
class KafkaMessage(BaseModel):
    version: Optional[str] = None
    topic: Optional[str] = None
    message_class: Optional[str] = None
    message_subclass: Optional[str] = None
    payload_metadata: Optional[str] = None
    payload_body: Optional[str] = None
    timestamp: Optional[datetime] = None
    origin_ip: Optional[str] = None


# Properties to receive via API on creation
class KafkaMessageCreate(KafkaMessage):
    version: str
    topic: str
    message_class: str
    message_subclass: str
    payload_metadata: str
    payload_body: str
    timestamp: datetime
    origin_ip: str


class KafkaMessageList(BaseModel):
    messages: List[KafkaMessageCreate]