from typing import List, Any

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from resources.route import api_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the application"}


@app.get("/health")
async def root():
    return {"message": f"Hello world"}

app.include_router(api_router)

BACKEND_CORS_ORIGINS: List[Any] = [
        "*"
    ]

app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
