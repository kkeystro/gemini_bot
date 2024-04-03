import aiohttp
import asyncio
import json
from db.redb import ReStorage
from serialiser import deserialise as d

storage = ReStorage(chat_id=67857)


async def generate_text(uid):
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyCzzvmLiQPhl0CHfq3fJYQXEqpGf5JCt4g"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [

            # {
            #     "parts": [
            #
            #         {
            #             "text": input_text
            #         }
            #     ],
            #     "role": "user"
            # },
            d(await storage.rangel(str(uid)))
        ],
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, headers=headers, data=json.dumps(payload)) as response:
            if response.status == 200:
                data = await response.json()
                for candidate in data.get("candidates", []):
                    text_parts = []
                    for part in candidate.get("content", {}).get("parts", []):
                        if "text" in part:
                            text_parts.append(part["text"])
                    return ''.join(text_parts)
                # print("Generated text:", data.get("candidates"))
            else:
                print("Error:", response.status, await response.text())

# asyncio.run(generate_text(input_text="What is the future of artificial intelligence?"))
