import os
from tinydb import TinyDB, Query
import bcrypt
import asyncio
from aio_pika import connect_robust, IncomingMessage, Message
import jwt
from jwt import InvalidTokenError

User = Query()
db = TinyDB('/etc/db/db.json')

if os.getenv("ENV") == "test":
    SECRET_KEY = 'testSecret'
else:
    SECRET_KEY = os.getenv("SECRET")
    
def createJWT(username):
    payload = {
        'username': username
    }
    
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verifyJWT(token):
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')

        if 'username' in decoded_payload and decoded_payload['username']:
            username = decoded_payload['username']

            db_user = db.search(User.username == username)

            if not db_user:
                return False
            else:
                return True
        else:
            return False
    except InvalidTokenError:
        return False
    
async def send_reply(reply: bytes, message: IncomingMessage):
    if message.reply_to:
        connection = await connect_robust("amqp://test:test@messagequeue:5672/")
        channel = await connection.channel()

        reply_message = Message(
            body=reply,
            correlation_id=message.correlation_id
        )

        await channel.default_exchange.publish(reply_message, routing_key=message.reply_to)
        await channel.close()
        await connection.close()

async def handle_registration(message: IncomingMessage):
    async with message.process():
        username, password = message.body.decode().split('|')

        if db.search(User.username == username):
            await send_reply(b"User already exists", message)
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        db.insert({'username': username, 'password': hashed_password.decode('utf-8')})

        await send_reply(createJWT(username).encode('utf-8'), message)

async def handle_login(message: IncomingMessage):
    async with message.process():
        username, password = message.body.decode().split('|')

        db_user = db.search(User.username == username)

        if not db_user:
            await send_reply(b"User not found", message)
            return

        db_user = db_user[0]
        if bcrypt.checkpw(password.encode('utf-8'), db_user['password'].encode('utf-8')):
            await send_reply(createJWT(username).encode('utf-8'), message)
        else:
            await send_reply(b"Invalid password", message)

async def handle_verification(message: IncomingMessage):
    async with message.process():
        valid = verifyJWT(message.body.decode())
        
        if valid:
            await send_reply(b"True", message)
        else:
            await send_reply(b"False", message)


async def consume():
    connection = await connect_robust("amqp://test:test@messagequeue:5672/")
    channel = await connection.channel()

    registration_queue = await channel.declare_queue('registration_queue', durable=True)
    login_queue = await channel.declare_queue('login_queue', durable=True)
    verify_queue = await channel.declare_queue('verify_queue', durable=True)

    await registration_queue.consume(handle_registration)
    await login_queue.consume(handle_login)
    await verify_queue.consume(handle_verification)

    print('[*] User-Management wartet auf Nachrichten. Zum Beenden CTRL+C drücken')
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(consume())
