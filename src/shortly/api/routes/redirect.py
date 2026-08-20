from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from shortly.core.database import get_db
from shortly.models.urls import URL
from shortly.utils.base62 import decode_base62

router = APIRouter(tags=["redirect"])


@router.get("/{short_url}")
async def redirect_url(
    short_url: str,
    db: Session = Depends(get_db),
):
    url_id = decode_base62(short_url)

    url = db.get(URL, url_id)

    if url is None:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found",
        )

    if url.expires_at and url.expires_at <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=410,
            detail="Short URL has expired",
        )

    return RedirectResponse(
        url=url.original_url,
        status_code=302,
    )
