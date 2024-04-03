import redis.asyncio as redis

client = redis.Redis(host='127.0.0.1', port=6379)


class ReStorage:

    def __init__(self, chat_id: int):
        self.chat_id = chat_id

    def _get_key(self, key: str):
        return str(self.chat_id) + key

    async def set_item(self, key: str, value):
        await client.set(name=self._get_key(key), value=value)

    async def get_item(self, key: str, default_value: str = None):
        value = await client.get(name=self._get_key(key))
        return value.decode() if value else default_value

    async def remove_item(self, key: str):
        await client.delete(self._get_key(key))

    async def pushl(self, key: str, value: str):
        await client.lpush(self._get_key(key), value)

    async def pushr(self, key: str, value: str):
        await client.rpush(self._get_key(key), value)

    async def rangel(self, key: str):
        return await client.lrange(self._get_key(key), 0, -1)

    async def delkey(self, key: str):
        await client.delete(self._get_key(key))