from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Token Engine")

app.include_router(router)

@app.get("/")
def home():
    return {"status": "running"}