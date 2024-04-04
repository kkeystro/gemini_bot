import aiosqlite
import asyncio
from datetime import datetime

DB_FILE = 'api_keys.db'


async def setup_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS api_key_usage (
                            key TEXT PRIMARY KEY,
                            usage_count_24h INTEGER DEFAULT 0,
                            last_usage_time TIMESTAMP
                        )''')
        await db.commit()


async def add_api_key(api_key):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('''INSERT OR IGNORE INTO api_key_usage (key, last_usage_time, usage_count_24h)
                            VALUES (?, ?, 0)
                        ''', (api_key, datetime.now()))
        await db.commit()


async def update_key_usage(api_key):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('''INSERT INTO api_key_usage (key, last_usage_time, usage_count_24h)
                            VALUES (?, ?, 1)
                            ON CONFLICT(key) DO UPDATE SET
                            usage_count_24h = usage_count_24h + 1,
                            last_usage_time = ?
                        ''', (api_key, datetime.now(), datetime.now()))
        await db.commit()


async def get_good_key():
    async with aiosqlite.connect(DB_FILE) as db:
        cur = await db.execute('''SELECT key FROM api_key_usage
                                  WHERE (strftime('%s', 'now') - strftime('%s', last_usage_time)) > 30
                                  AND usage_count_24h <= 1000
                                  ORDER BY last_usage_time ASC
                                  LIMIT 1
                               ''')
        row = await cur.fetchone()
        await update_key_usage(row[0])
        return row[0] if row else "AIzaSyCzzvmLiQPhl0CHfq3fJYQXEqpGf5JCt4g"


async def reset_daily_counts():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('UPDATE api_key_usage SET usage_count_24h = 0')
        await db.commit()


async def auto_reset_daily_counts():
    while True:
        await asyncio.sleep(86400)  # Wait for 24 hours (86400 seconds)
        await reset_daily_counts()


async def main():
    await setup_db()


asyncio.run(main())
