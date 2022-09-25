# https://fastapi.tiangolo.com/tutorial/bigger-applications/
# https://fastapi.tiangolo.com/tutorial/body/
from fastapi import FastAPI
from pydantic import BaseModel
# this is required to be able to access the fastapi server from VUE.js on another port
from fastapi.middleware.cors import CORSMiddleware


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # frontend address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api")
async def send_expression(item: Item):
    item.description = item.description + "hi"
    return item


@app.get("/")
def home():
    return "FastAPI GET"
