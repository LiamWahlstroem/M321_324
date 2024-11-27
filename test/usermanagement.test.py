import pytest
import asyncio
from aio_pika import connect_robust, Message
from aio_pika.patterns import RPC
import jwt

RABBITMQ_URL = "amqp://test:test@localhost:5672/"
SECRET_KEY = 'testSecret'

@pytest.mark.asyncio
async def test_registration_and_login():
    # Connect to RabbitMQ
    connection = await connect_robust(RABBITMQ_URL)
    channel = await connection.channel()

    # Declare registration and login queues
    registration_queue = await channel.declare_queue('registration_queue', durable=True)
    login_queue = await channel.declare_queue('login_queue', durable=True)

    # Test registration flow
    username = "testuser"
    password = "testpassword"
    registration_message = f"{username}|{password}".encode()

    async def on_registration_reply(message):
        response = message.body.decode()
        assert response == "User registered successfully"
        await message.ack()

    # Publish registration message and wait for response
    await channel.default_exchange.publish(
        Message(body=registration_message, reply_to="registration_reply_queue"),
        routing_key=registration_queue.name
    )

    # Test login flow
    login_message = f"{username}|{password}".encode()

    async def on_login_reply(message):
        response = message.body.decode()

        # Verify the JWT token
        decoded_payload = jwt.decode(response, SECRET_KEY, algorithms="HS256")
        assert decoded_payload['username'] == username

        await message.ack()