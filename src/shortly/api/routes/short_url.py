from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from shortly.core.database import get_db
from shortly.models.requests import LongUrl
from shortly.models.urls import URL
from shortly.utils.base62 import encode_base62

router = APIRouter(tags=["short-url-api"])


@router.post(
    "/api/shorten",
    status_code=status.HTTP_201_CREATED,
)
async def shorten(
    request: LongUrl,
    req: Request,
    db: Session = Depends(get_db),
):
    long_url = str(request.url)

    expire_time = datetime.now(timezone.utc) + timedelta(hours=12)

    # First save URL and get database ID
    url = URL(
        original_url=long_url,
        expires_at=expire_time,
        short_code="",  # temporary
    )

    db.add(url)
    db.commit()
    db.refresh(url)

    # Convert DB ID → Base62
    short_code = encode_base62(url.id)

    # Store short code
    url.short_code = short_code

    db.commit()
    db.refresh(url)

    return {
        "short_url": f"{req.base_url}{short_code}",
        "expires_at": url.expires_at,
    }