import os
from tinydb import TinyDB, Query
import bcrypt
import asyncio
from aio_pika import connect_robust, IncomingMessage
import jwt

User = Query()

if os.getenv("ENV") == "test":
    SECRET_KEY = 'testSecret'
    db = TinyDB('./db.json')
else:
    SECRET_KEY = os.getenv("SECRET")
    db = TinyDB('/etc/db/db.json')

def createJWT(username):
    payload = {
        'username': username
    }
    
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verifyJWT(jwt):
    try:
        decoded_payload = jwt.decode(jwt, SECRET_KEY, algorithms='HS256')

        if 'username' in decoded_payload and decoded_payload['username']:
            username = decoded_payload['username']

            db_user = db.search(User.username == username)

            if not db_user:
                return False
            else:
                return True

        else:
            return False
    except jwt.InvalidTokenError:
        return False

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
            await message.reply(createJWT(username))
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
