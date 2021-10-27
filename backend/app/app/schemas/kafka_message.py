from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


# Shared properties
class KafkaMessageBase(BaseModel):
    session_id: Optional[int] = None
    user_id: Optional[int] = None
    case_id: Optional[int] = None
    knot_id: Optional[int] = None
    timestamp: Optional[datetime] = None
    hipothesis: Optional[str] = None
    origin_ip: Optional[str] = None


# Properties to receive via API on creation
class KafkaMessageCreate(KafkaMessageBase):
    session_id: int
    user_id: int
    case_id: int
    knot_id: int
    timestamp: datetime
    hipothesis: str


class KafkaMessage(KafkaMessageBase):
    pass