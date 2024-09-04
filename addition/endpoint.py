#!/usr/bin/python

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AdditionInput(BaseModel):
    num1: int
    num2: int

@app.post("/addition")
async def addition(input_data: AdditionInput):
    return {"result": input_data.num1 + input_data.num2}
