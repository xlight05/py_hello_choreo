from fastapi import FastAPI

api = FastAPI()


@api.get("/")
async def root():
    return {"message": "Hello World"}

@api.post("/ask")
async def ask():
    return {"resp": "Hello World"}
