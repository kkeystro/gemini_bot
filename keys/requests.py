import asyncio
import time
from keys.models import APIKeyUsage, Session
from sqlalchemy import func, select, update


async def add_api_key(api_key):
    async with Session() as session:
        async with session.begin():
            new_key = APIKeyUsage(key=api_key, last_usage_time=int(time.time()))
            session.add(new_key)


async def update_key_usage(api_key):
    async with Session() as session:
        async with session.begin():
            result = await session.execute(select(APIKeyUsage).filter_by(key=api_key))
            key_usage = result.scalars().first()
            if key_usage:
                key_usage.usage_count_24h += 1
                key_usage.last_usage_time = int(time.time())


async def get_good_key():
    async with Session() as session:
        async with session.begin():
            result = await session.execute(
                select(APIKeyUsage).filter(
                    (func.strftime('%s', 'now') - APIKeyUsage.last_usage_time) > 3,
                    APIKeyUsage.usage_count_24h <= 1000
                ).order_by(APIKeyUsage.last_usage_time.asc())
            )
            key_usage = result.scalars().first()
            if key_usage:
                await update_key_usage(key_usage.key)
                return str(key_usage.key)
    return "High load, please wait"


async def show_good_keys():
    async with Session() as session:
        async with session.begin():
            result = await session.execute(
                select(APIKeyUsage).filter(
                    (func.strftime('%s', 'now') - APIKeyUsage.last_usage_time) > 30,
                    APIKeyUsage.usage_count_24h <= 1000
                ).order_by(APIKeyUsage.last_usage_time.asc())
            )
            key_usage = result.scalars().fetchall()
            if key_usage:
                return str(key_usage)
    return "High load, please wait"


async def reset_daily_counts():
    async with Session() as session:
        async with session.begin():
            await session.execute(
                update(APIKeyUsage).values(usage_count_24h=0)
            )


async def auto_reset_daily_counts():
    while True:
        await asyncio.sleep(86400)  # Ждем 24 часа (86400 секунд)
        await reset_daily_counts()
