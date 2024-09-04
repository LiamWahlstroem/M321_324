#!/usr/bin/python

from fastapi import FastAPI
from pydantic import BaseModel

class AdditionInput(BaseModel):
    num1: int
    num2: int

app = FastAPI()

@app.post("/addition")
async def addition(input_data: AdditionInput):
    return {"result": input_data.num1 + input_data.num2}
