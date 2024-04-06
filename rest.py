import aiohttp
import json
from db.redb import ReStorage
from serialiser import deserialise as d
from keys.keysdb import get_good_key as key

storage = ReStorage(chat_id=67857)


async def generate_text(uid):
    akey=str(await key())
    if akey != "High load, please wait 30 seconds":
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={akey}"
    else:
        return "High load, please wait 30 seconds"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [
            d(await storage.rangel(str(uid)))
        ],
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, headers=headers, data=json.dumps(payload)) as response:
            if response.status == 200:
                data = await response.json()
                if not "Error" in data.keys():
                    for candidate in data.get("candidates", []):
                        text_parts = []
                        for part in candidate.get("content", {}).get("parts", []):
                            if "text" in part:
                                text_parts.append(part["text"])
                        if text_parts:
                            return ''.join(text_parts)
                        else:
                            return "Ur momma gay"
                else:
                    print("Error:", response.status, await response.text())
                    return "Error"
            else:
                print("Error:", response.status, await response.text())
                return "Error"
