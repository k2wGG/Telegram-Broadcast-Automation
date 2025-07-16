from apscheduler.schedulers.blocking import BlockingScheduler
from dispatcher import send_post_to_channels
from channel_db import get_channels
from datetime import datetime
import os
import json
import traceback

POSTS_FILE = "scheduled_posts.json"
scheduler = BlockingScheduler()


def load_scheduled_posts():
    if os.path.exists(POSTS_FILE):
        try:
            with open(POSTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print("⚠️ Ошибка при загрузке scheduled_posts.json:", e)
            return []
    return []



def save_scheduled_posts(posts):
    with open(POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)


def schedule_post(text: str, datetime_obj, file_path: str = None):
    if isinstance(datetime_obj, datetime):
        datetime_str = datetime_obj.isoformat()
    else:
        datetime_str = str(datetime_obj)

    posts = load_scheduled_posts()
    post = {
        "text": text,
        "time": datetime_str,
        "file_path": file_path
    }
    posts.append(post)
    save_scheduled_posts(posts)



def check_and_send_posts():
    print("⏰ Проверка запланированных постов...")
    try:
        posts = load_scheduled_posts()
        now = datetime.now().isoformat()
        remaining = []

        for post in posts:
            if post["time"] <= now:
                print(f"📤 Отправка поста: {post['text'][:30]}...")
                try:
                    send_args = [post["text"], post.get("file_path")]
                    import asyncio
                    asyncio.run(send_post_to_channels(*send_args))
                except Exception as send_err:
                    print("Ошибка при отправке:", send_err)
                    traceback.print_exc()
            else:
                remaining.append(post)

        save_scheduled_posts(remaining)

    except Exception as e:
        print("❌ Ошибка в планировщике:")
        traceback.print_exc()


def start_scheduler():
    scheduler.add_job(check_and_send_posts, "interval", minutes=1)
    scheduler.start()
