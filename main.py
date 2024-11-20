from fastapi import FastAPI
from parser.vk import main

app = FastAPI()


@app.get("/")
async def root():
    return {"message": 'Hello World'}


@app.get("/video")
async def root():
    result = await main()
    return {"message": result}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
