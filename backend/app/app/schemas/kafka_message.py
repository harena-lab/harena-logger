from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class KafkaMessageBase(BaseModel):
    case: Optional[int] = None
    payload: Optional[str] = None
    origin_ip: Optional[str] = None
    event: Optional[str] = 'default event'


# Properties to receive via API on creation
class KafkaMessageCreate(KafkaMessageBase):
    case: int
    payload: str


class KafkaMessage(KafkaMessageBase):
    pass