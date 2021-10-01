from typing import Any

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app import models, schemas
from app.api import deps
from app.core.celery_app import celery_app
from app.utils import send_test_email
import json

from mongoengine import connect, Document, BooleanField, ObjectIdField, StringField

router = APIRouter()

class Test2(Document):
    _id = ObjectIdField()
    name = StringField()


@router.post("/test-mongodb/", response_model=schemas.Msg, status_code=201)
def test_mongodb(
    msg: schemas.Msg,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test Celery worker.
    """
    # TODO: remove credentials from here and init db
    print("testing")
    connect(db='logger-dev', host='mongo', port=27017, username='logger', password='harena')
    input = Test2(name=msg.msg)
    input.save()
    test_json = json.loads(Test2.objects().to_json())
    print(test_json)
    return {"msg": str(test_json)}

@router.post("/test-celery/", response_model=schemas.Msg, status_code=201)
def test_celery(
    msg: schemas.Msg,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test Celery worker.
    """
    celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}


@router.post("/test-email/", response_model=schemas.Msg, status_code=201)
def test_email(
    email_to: EmailStr,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}
