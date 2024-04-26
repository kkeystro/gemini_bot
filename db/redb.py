import redis.asyncio as redis

client = redis.Redis(host='127.0.0.1', port=6379)


async def pushr(key: str, value: str):
    await client.rpush(key, value)


async def rangel(key: str):
    return await client.lrange(key, 0, -1)


async def delkey(key: str):
    await client.delete(key)


async def set_ul(key: str):
    await client.set(key + '_ul', 1)


async def unlock(key: str):
    await client.set(key + '_ul', 0)


async def check_ul(key: str):
    if await client.get(key + '_ul') == 1:
        return True
    else:
        return False
