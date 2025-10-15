from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .database import engine, SessionLocal
from .models import Base
from .main import router as api_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Battery Energy Storage Optimization API",
    version="1.0.0",
    description="Modular and fully DB-driven BESS optimization API",
)

app.include_router(api_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with allowed frontend domains in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

__all__ = ["app", "get_db"]
