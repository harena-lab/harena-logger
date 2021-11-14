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
    kafka_message_document = models.KafkaMessageRecord(version=kafka_message_in.version, topic=kafka_message_in.topic,
                                     message_class=kafka_message_in.message_class, message_subclass=kafka_message_in.message_subclass,
                                     payload_metadata=kafka_message_in.payload_metadata, payload_body=kafka_message_in.payload_body,
                                    timestamp=kafka_message_in.timestamp, origin_ip=kafka_message_in.origin_ip)


    synchronousSend(kafka_message_document.message_class, kafka_message_document)
    return kafka_message_in
