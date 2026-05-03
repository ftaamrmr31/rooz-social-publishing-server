from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.publish_job import PublishJob
from app.schemas.publish_job import (
    PublishJobCreate,
    PublishJobRead,
    TelegramSendNowRequest,
)
from app.integrations.telegram_publisher import send_telegram_message
from app.core.api_key import verify_api_key

publish_router = APIRouter()


@publish_router.post("", response_model=PublishJobRead, dependencies=[Depends(verify_api_key)])
def create_publish_job(job: PublishJobCreate, db: Session = Depends(get_db)):
    db_job = PublishJob(
        platform=job.platform,
        content=job.content,
        status="pending"
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@publish_router.get("", response_model=List[PublishJobRead])
def get_publish_jobs(db: Session = Depends(get_db)):
    return db.query(PublishJob).all()


@publish_router.post("/telegram/send-now", dependencies=[Depends(verify_api_key)])
def send_now_telegram(request: TelegramSendNowRequest):
    try:
        result = send_telegram_message(request.content)
        return {
            "success": True,
            "platform": "telegram",
            "result": result
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
