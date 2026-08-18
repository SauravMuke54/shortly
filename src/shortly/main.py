from fastapi import FastAPI

from shortly.api.router import api_router

app = FastAPI(root_path="/", docs_url="/docs", redoc_url="/redocs")

app.include_router(router=api_router)


@app.get("/health")
def health():
    return {"status": "ok"}
