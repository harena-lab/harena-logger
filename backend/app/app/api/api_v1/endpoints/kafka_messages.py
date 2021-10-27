from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.kafka_app import synchronousSend

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
    kafka_message_document = models.KafkaMessageRecord(session_id=kafka_message_in.session_id, user_id=kafka_message_in.user_id, case_id=kafka_message_in.case_id, knot_id=kafka_message_in.knot_id, timestamp=kafka_message_in.timestamp, hipothesis=kafka_message_in.hipothesis, origin_ip=kafka_message_in.origin_ip)
    synchronousSend('log_raw_default', kafka_message_document)
    return kafka_message_in
