from fastapi import FastAPI
from resources.route import api_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the application"}


@app.get("/health")
async def root():
    return {"message": f"Hello world"}


app = FastAPI()
app.include_router(api_router)
