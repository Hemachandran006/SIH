from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import auth, devices, wipes, certificates
from app.seed import seed_demo

import os

app = FastAPI(title="WipeChain API", version="0.1.0")

origins = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "*").split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
seed_demo()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(devices.router, prefix="/devices", tags=["devices"])
app.include_router(wipes.router, prefix="/wipes", tags=["wipes"])
app.include_router(certificates.router, prefix="/certificates", tags=["certificates"])

@app.get("/health")
def health():
    return {"status": "ok"}