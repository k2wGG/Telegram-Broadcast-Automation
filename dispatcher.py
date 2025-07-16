from telethon import TelegramClient
from channel_db import get_channels
from config import API_ID, API_HASH

async def send_post_to_channels(text, file_path=None):
    # создаём клиент с уникальной сессией в памяти (без файла)
    client = TelegramClient("session_for_scheduler", API_ID, API_HASH)

    await client.connect()

    if not await client.is_user_authorized():
        print("⛔ Клиент не авторизован — нужно пройти логин один раз вручную!")
        await client.disconnect()
        return

    channels = get_channels()
    for channel_id, _ in channels:
        try:
            if file_path:
                await client.send_file(channel_id, file_path, caption=text, parse_mode="html")
            else:
                await client.send_message(channel_id, text, parse_mode="html")
        except Exception as e:
            print(f"Ошибка при отправке в {channel_id}: {e}")

    await client.disconnect()
