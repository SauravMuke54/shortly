from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from shortly.api.router import api_router
from shortly.core.database import Base, engine

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url="/docs", redoc_url="/redocs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=api_router)


@app.get("/health")
def health():
    return {"status": "ok"}
