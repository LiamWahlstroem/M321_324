from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SubtractInput(BaseModel):
    num1: int
    num2: int

@app.post("/subtract")
async def subtract(input_data: SubtractInput):
    return {"result": input_data.num1 - input_data.num2}
