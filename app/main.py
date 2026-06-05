from fastapi import FastAPI

from app.db.database import engine
from sqlalchemy import text

app = FastAPI(
    title="Book Management System"
)


@app.get("/")
async def root():
    return {
        "message": "Hello World!!!!"
    }

@app.get("/db")
async def health_db():

    async with engine.connect() as conn:
        result = await conn.execute(
            text("SELECT 1")
        )

    return {"result": result.scalar()}
