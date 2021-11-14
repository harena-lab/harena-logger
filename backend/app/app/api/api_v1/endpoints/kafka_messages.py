from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.kafka_app import synchronousSend

from datetime import datetime

router = APIRouter()

@router.post("/", response_model=schemas.KafkaMessage)
def create_kafka_message(
    *,
    kafka_message_in: schemas.KafkaMessageCreate,
    request: Request
) -> Any:
    """
    Create new kafka_message.
    """

    kafka_message_in.origin_ip = request.client.host
    kafka_message_in.timestamp = datetime.now()
    kafka_message_document = models.KafkaMessageRecord(version=kafka_msg.version, topic=kafka_msg.topic,
                                     message_class=kafka_msg.message_class, message_subclass=kafka_msg.message_subclass,
                                     payload_metadata=kafka_msg.payload_metadata, payload_body=kafka_msg.payload_body,
                                    timestamp=kafka_msg.timestamp, origin_ip=kafka_msg.origin_ip)


    synchronousSend(kafka_message_document.message_class, kafka_message_document)
    return kafka_message_in
