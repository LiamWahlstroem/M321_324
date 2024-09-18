from tinydb import TinyDB, Query
import bcrypt
import asyncio
from aio_pika import connect_robust, IncomingMessage

db = TinyDB('db.json')
User = Query()

async def handle_registration(message: IncomingMessage):
    async with message.process():
        username, password = message.body.decode().split('|')

        if db.search(User.username == username):
            await message.reply(b"User already exists")
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        db.insert({'username': username, 'password': hashed_password})

        await message.reply(b"User registered successfully")

async def handle_login(message: IncomingMessage):
    async with message.process():
        username, password = message.body.decode().split('|')

        db_user = db.search(User.username == username)

        if not db_user:
            await message.reply(b"User not found")
            return

        db_user = db_user[0]
        if bcrypt.checkpw(password.encode('utf-8'), db_user['password']):
            await message.reply(b"Login successful")
        else:
            await message.reply(b"Invalid password")

async def consume():
    connection = await connect_robust("amqp://test:test@messagequeue:5672/")
    channel = await connection.channel()

    registration_queue = await channel.declare_queue('registration_queue', durable=True)
    login_queue = await channel.declare_queue('login_queue', durable=True)

    await registration_queue.consume(handle_registration)
    await login_queue.consume(handle_login)

    print(' [*] User-Management wartet auf Nachrichten. Zum Beenden CTRL+C drücken')
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(consume())
