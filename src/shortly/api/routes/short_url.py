from fastapi import APIRouter
from shortly.models.requests import LongUrl

router = APIRouter(tags=["short-url-api"])

@router.post("/api/shorten")
async def shorten(request:LongUrl):
    return request.url.split(".")


