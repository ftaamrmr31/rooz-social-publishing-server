# PublishJob API endpoints

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.publish_job import PublishJob
from app.schemas.publish_job import PublishJobCreate, PublishJobRead

# Create a router for publish job endpoints.
# This router is registered in app/api/router.py with the "/publish" prefix.
publish_router = APIRouter()


@publish_router.post(
    "",
    response_model=PublishJobRead,
    summary="Create a new publish job",
)
def create_publish_job(
    job_in: PublishJobCreate,
    db: Session = Depends(get_db),
):
    """
    Receive a platform and content, create a PublishJob record with
    status "pending", save it to the database, and return the saved record.
    """
    job = PublishJob(
        platform=job_in.platform,
        content=job_in.content,
        status="pending",
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@publish_router.get(
    "",
    response_model=list[PublishJobRead],
    summary="List all publish jobs",
)
def list_publish_jobs(
    db: Session = Depends(get_db),
):
    """
    Return all PublishJob records stored in the database.
    """
    jobs = db.query(PublishJob).all()
    return jobs
