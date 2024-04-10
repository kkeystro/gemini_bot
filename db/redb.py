import redis.asyncio as redis

client = redis.Redis(host='127.0.0.1', port=6379)


async def pushr(key: str, value: str):
    await client.rpush(key, value)

async def rangel(key: str):
    return await client.lrange(key, 0, -1)

async def delkey(key: str):
    await client.delete(key)
