from fastapi import APIRouter

from shortly.api.routes import redirect, short_url

api_router = APIRouter()

api_router.include_router(short_url.router)
api_router.include_router(redirect.router)
