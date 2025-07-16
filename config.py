# config.py

from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')

SESSION_NAME = os.getenv('SESSION_NAME', 'session/main')
DB_PATH = os.getenv('DB_PATH', 'channels.db')
POSTS_FOLDER = os.getenv('POSTS_FOLDER', 'posts')
