# bot.py

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import BOT_TOKEN, ADMIN_ID, POSTS_FOLDER
from channel_db import init_db, add_channel, remove_channel, get_channels
import os

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Инициализируем базу
init_db()

# Проверка доступа
def is_admin(message: types.Message):
    return message.from_user.id == ADMIN_ID

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    if not is_admin(message):
        return
    await message.answer("Привет! Я бот для рассылки.\nКоманды:\n/addchannel\n/list\n/post\n/deletechannel")

@dp.message(Command("addchannel"))
async def add_channel_handler(message: types.Message):
    if not is_admin(message):
        return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            await message.reply("Используй так: /addchannel <channel_id или @username> [название]")
            return

        raw_id = parts[1]
        # Поддержка @username и чисел
        if raw_id.lstrip("-").isdigit():
            channel_id = int(raw_id)
        else:
            channel_id = raw_id  # сохраняем как строку

        name = ' '.join(parts[2:]) if len(parts) > 2 else None
        add_channel(channel_id, name)
        await message.reply("Канал добавлен.")
    except Exception as e:
        await message.reply(f"Ошибка: {e}")


@dp.message(Command("deletechannel"))
async def delete_channel_handler(message: types.Message):
    if not is_admin(message):
        return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            await message.reply("Используй так: /deletechannel <channel_id или @username>")
            return

        raw_id = parts[1]
        channel_id = int(raw_id) if raw_id.lstrip("-").isdigit() else raw_id
        remove_channel(channel_id)
        await message.reply("Канал удалён.")
    except Exception as e:
        await message.reply(f"Ошибка: {e}")


@dp.message(Command("list"))
async def list_channels_handler(message: types.Message):
    if not is_admin(message):
        return
    channels = get_channels()
    if not channels:
        await message.reply("Список каналов пуст.")
        return
    msg = "\n".join([f"{cid} — {name or 'Без названия'}" for cid, name in channels])
    await message.reply(f"Список каналов:\n{msg}")

@dp.message(Command("post"))
async def post_message_handler(message: types.Message):
    if not is_admin(message):
        return
    files = os.listdir(POSTS_FOLDER)
    text_files = [f for f in files if f.endswith('.txt')]

    if not text_files:
        await message.reply("Нет доступных файлов в папке posts.")
        return

    menu = "\n".join(f"{i+1}. {f}" for i, f in enumerate(text_files))
    await message.reply(f"Выбери файл для отправки:\n{menu}\n\nОтправь номер файла:")

    @dp.message()
    async def get_file_number(msg: types.Message):
        try:
            idx = int(msg.text.strip()) - 1
            filename = text_files[idx]
            filepath = os.path.join(POSTS_FOLDER, filename)

            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()

            channels = get_channels()
            count = 0
            for channel_id, _ in channels:
                try:
                    await bot.send_message(channel_id, text, parse_mode="HTML")
                    count += 1
                except Exception as e:
                    await message.reply(f"Ошибка в {channel_id}: {e}")

            await msg.reply(f"Пост отправлен в {count} каналов.")
        except Exception as e:
            await msg.reply(f"Ошибка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
