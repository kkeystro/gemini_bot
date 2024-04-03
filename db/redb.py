import redis.asyncio as redis

client = redis.Redis(host='127.0.0.1', port=6379)


class ReStorage:

    def __init__(self, chat_id: int):
        self.chat_id = chat_id

    def _get_key(self, key: str):
        return str(self.chat_id) + key

    async def pushr(self, key: str, value: str):
        await client.rpush(self._get_key(key), value)

    async def rangel(self, key: str):
        return await client.lrange(self._get_key(key), 0, -1)

    async def delkey(self, key: str):
        await client.delete(self._get_key(key))
