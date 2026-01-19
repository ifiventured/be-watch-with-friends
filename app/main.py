from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="FastAPI Spike")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/echo/{msg}")
def echo(msg: str, shout: bool = False):
    return {"msg": msg.upper() if shout else msg}

class Item(BaseModel):
    name: str
    qty: int = 1

@app.post("/items", status_code=201)
def create_item(item: Item):
    return {"created": item.model_dump()}
