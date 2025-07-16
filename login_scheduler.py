from telethon import TelegramClient
from config import API_ID, API_HASH

client = TelegramClient("session_for_scheduler", API_ID, API_HASH)

async def main():
    await client.start()
    print("✅ Готово. Сессия авторизована!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())