from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from aio_pika import connect_robust, Message
import uuid


app = FastAPI()

class MultiplicationInput(BaseModel):
    num1: int
    num2: int
    jwt: str

@app.post("/multiplication")
async def multiplication(input_data: MultiplicationInput):
    correlation_id = str(uuid.uuid4())
    connection = await connect_robust("amqp://test:test@messagequeue:5672/")
    channel = await connection.channel()
    response_queue = await channel.declare_queue(exclusive=True)

    message = Message(
        body=input_data.jwt.encode(),
        reply_to=response_queue.name,
        correlation_id=correlation_id,
    )

    await channel.default_exchange.publish(message, routing_key="verify_queue")

    async with response_queue.iterator() as queue_iter:
        async for response_message in queue_iter:
            if response_message.correlation_id == correlation_id:
                if response_message.body.decode() == "True":
                    return {"result": input_data.num1 * input_data.num2}
                else:
                    raise HTTPException(status_code=401, detail="User Not authorized")
