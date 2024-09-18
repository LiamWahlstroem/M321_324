from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from aio_pika import connect_robust, Message
import uuid

app = FastAPI()

class LoginUser(BaseModel):
    username: str
    password: str

async def send_login_request(user: LoginUser):
    correlation_id = str(uuid.uuid4())
    connection = await connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()

    response_queue = await channel.declare_queue(exclusive=True)

    message = Message(
        body=f"{user.username}|{user.password}".encode(),
        reply_to=response_queue.name,
        correlation_id=correlation_id,
    )

    await channel.default_exchange.publish(message, routing_key="login_queue")

    async with response_queue.iterator() as queue_iter:
        async for response_message in queue_iter:
            if response_message.correlation_id == correlation_id:
                return response_message.body.decode()

@app.post("/login")
async def login_user(user: LoginUser):
    response = await send_login_request(user)

    if response == "User not found":
        raise HTTPException(status_code=404, detail="User not found")
    elif response == "Invalid password":
        raise HTTPException(status_code=400, detail="Invalid password")

    return {"message": response}
