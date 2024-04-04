import aiohttp


async def check_key(key):
    url = f"https://ai.google.dev/api/rest/v1beta/models/list?key={str(key)}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return True
            return False

