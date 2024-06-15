from fastapi import FastAPI

api = FastAPI()


@api.get("/")
async def root():
    return {"message": "Hello World"}

@api.post("/ask")
async def root():
    return {"resp": "Hello World"}
