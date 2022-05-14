from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    foo: str
    bar: str


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/item")
def item(foo: str = 'none', bar: str='none'):
    return {"status": 200, "foo": foo, "bar": bar}