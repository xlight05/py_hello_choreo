from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/ask")
async def root():
    return {"resp": "Hello World"}
