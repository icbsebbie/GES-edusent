from fastapi import FastAPI
from .db import Base, engine
from .api.router import router

app = FastAPI(title="GES EduSentinel API")
Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/health")
def health():
    return {"ok": True}
