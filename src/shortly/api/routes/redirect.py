from fastapi import APIRouter

router = APIRouter(tags=["redirect"])

@router.get("/{short_url}")
async def redirect_url():
    return "redirected"