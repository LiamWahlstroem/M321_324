from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class DivisionInput(BaseModel):
    num1: int
    num2: int

@app.post("/division")
async def division(input_data: DivisionInput):
    return {"result": input_data.num1 / input_data.num2}
