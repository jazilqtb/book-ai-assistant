from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

# Cukup impor dari app.db
from app.db import get_db, redis_client

app = FastAPI(title="Book AI Assistant")

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    db_status = False
    try:
        result = await db.execute(text("SELECT 1"))
        if result.scalar() == 1:
            db_status = True
    except Exception as e:
        db_status = str(e)

    redis_status = False
    try:
        redis_status = await redis_client.ping()
    except Exception as e:
        redis_status = str(e)

    return {
        "status": "online",
        "postgres_connected": db_status,
        "redis_connected": redis_status
    }