from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.publish_job import PublishJob
from app.schemas.publish_job import PublishJobCreate, PublishJobRead

publish_router = APIRouter()


@publish_router.post("", response_model=PublishJobRead)
def create_publish_job(job: PublishJobCreate, db: Session = Depends(get_db)):
    # Create a new PublishJob ORM object with status set to "pending"
    db_job = PublishJob(
        platform=job.platform,
        content=job.content,
        status="pending",
    )
    # Save the record to the database
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@publish_router.get("", response_model=List[PublishJobRead])
def get_publish_jobs(db: Session = Depends(get_db)):
    # Return all publish job records from the database
    return db.query(PublishJob).all()
