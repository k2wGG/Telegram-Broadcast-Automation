from telethon import TelegramClient
import asyncio
from config import API_ID, API_HASH, SESSION_NAME

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def main():
    await client.start()
    await client.send_message(
        '@testparserbotds',
        '<b>Привет!</b> <a href="https://t.me/nod3r">ПОДПИШИСЬ</a>',
        parse_mode='html'
    )
    await client.disconnect()

asyncio.run(main())
