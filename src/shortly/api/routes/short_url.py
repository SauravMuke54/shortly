from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from shortly.core.database import get_db
from shortly.models.requests import LongUrl
from shortly.models.urls import URL, url_id_seq
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

    # Pull the next id from the DB sequence up front so we can encode
    # short_code before the row is ever written. One insert, no
    # placeholder value, no window where short_code is empty/duplicate.
    next_id = db.execute(url_id_seq).scalar()
    short_code = encode_base62(next_id)

    url = URL(
        id=next_id,
        original_url=long_url,
        expires_at=expire_time,
        short_code=short_code,
    )

    db.add(url)
    db.commit()
    db.refresh(url)

    return {
        "short_url": f"{req.base_url}{short_code}",
        "expires_at": url.expires_at,
    }