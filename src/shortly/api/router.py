from fastapi import APIRouter
from shortly.api.routes import short_url, redirect

api_router = APIRouter()

api_router.include_router(short_url.router)
api_router.include_router(redirect.router)