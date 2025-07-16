# channel_db.py

import sqlite3
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id INTEGER UNIQUE NOT NULL,
            name TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_channel(channel_id: int, name: str = None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO channels (channel_id, name)
        VALUES (?, ?)
    ''', (channel_id, name))
    conn.commit()
    conn.close()

def remove_channel(channel_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM channels WHERE channel_id = ?
    ''', (channel_id,))
    conn.commit()
    conn.close()

def get_channels():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT channel_id, name FROM channels')
    result = cursor.fetchall()
    conn.close()
    return result
