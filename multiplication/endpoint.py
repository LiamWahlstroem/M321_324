from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class MultiplicationInput(BaseModel):
    num1: int
    num2: int

@app.post("/multiplication")
async def multiplication(input_data: MultiplicationInput):
    return {"result": input_data.num1 * input_data.num2}
