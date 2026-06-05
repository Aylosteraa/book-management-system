from fastapi import FastAPI

app = FastAPI(
    title="Book Management System"
)


@app.get("/")
async def root():
    return {
        "message": "Hello World!!!!"
    }
