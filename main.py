from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/")
async def post_root():
    return {"message": "Hello from Post route"}


@app.put("/")
async def put_route():
    return {"message": "Hello from Put route"}
