from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
import os

app = FastAPI(title="AI Agent Discovery API")

# Allow CORS for all origins (for deployment)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# To run: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
