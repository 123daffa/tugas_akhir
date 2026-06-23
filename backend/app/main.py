from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Hoax Detection API")

app.include_router(router, prefix="/api")

@app.get("/")
def health_check():
    return {"status": "running"}