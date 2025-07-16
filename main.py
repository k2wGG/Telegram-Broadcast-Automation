import asyncio
from bot import dp, bot
from channel_db import init_db
import uvicorn
from multiprocessing import Process
from scheduler import start_scheduler


def run_web():
    uvicorn.run("web.main:app", host="0.0.0.0", port=8080, reload=False)


def run_scheduler():
    print("🔁 Планировщик запускается...")
    start_scheduler()


async def run_bot():
    print("🚀 Бот запускается...")
    init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Запускаем веб-сервер и планировщик в отдельных процессах
    web_process = Process(target=run_web)
    scheduler_process = Process(target=run_scheduler)

    web_process.start()
    scheduler_process.start()

    try:
        # Бот запускается в основном процессе
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print("⛔ Остановка...")
    finally:
        web_process.terminate()
        scheduler_process.terminate()

        web_process.join()
        scheduler_process.join()
