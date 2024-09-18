from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from aio_pika import connect_robust, Message
import uuid


app = FastAPI()

class RegisterUser(BaseModel):
    username: str
    password: str

async def send_registration_request(user: RegisterUser):
    correlation_id = str(uuid.uuid4())
    connection = await connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()

    response_queue = await channel.declare_queue(exclusive=True)

    message = Message(
        body=f"{user.username}|{user.password}".encode(),
        reply_to=response_queue.name,
        correlation_id=correlation_id,
    )

    await channel.default_exchange.publish(message, routing_key="registration_queue")

    async with response_queue.iterator() as queue_iter:
        async for response_message in queue_iter:
            if response_message.correlation_id == correlation_id:
                return response_message.body.decode()

@app.post("/register")
async def register_user(user: RegisterUser):
    response = await send_registration_request(user)

    if response == "User already exists":
        raise HTTPException(status_code=400, detail="User already exists")
    return {"message": response}

