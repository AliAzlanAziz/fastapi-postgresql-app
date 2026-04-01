from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.routers.auth import router as auth_router
from app.routers.education import router as education_router

from app.db import get_session
from app.models import *  # ensures models are imported so metadata knows about them

app = FastAPI()

@app.get("/")
async def hello_world():
    return {"message": "Hello World!"}

@app.get("/health")
async def health(db: AsyncSession = Depends(get_session)):
    # Simple DB check
    result = await db.execute(text("SELECT 1"))
    ok = bool(result.scalar())
    return {"status": "ok" if ok else "fail"}

app.include_router(auth_router)
app.include_router(education_router)