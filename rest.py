import aiohttp
import asyncio
import json
from os import environ


async def generate_text(input_text):
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyCzzvmLiQPhl0CHfq3fJYQXEqpGf5JCt4g"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [

            {
                "parts": [

                    {
                        "text": input_text
                    }

                ]
            }
        ],
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, headers=headers, data=json.dumps(payload)) as response:
            if response.status == 200:
                data = await response.json()
                for candidate in data.get("candidates", []):
                    text_parts = []
                    for part in candidate.get("content", {}).get("parts", []):
                        # Append the text of each part to the list
                        if "text" in part:
                            text_parts.append(part["text"])
                    # Join all text parts for this candidate and print
                    return ''.join(text_parts)
                #print("Generated text:", data.get("candidates"))
            else:
                print("Error:", response.status, await response.text())


# Run the async function
#asyncio.run(generate_text(input_text="What is the future of artificial intelligence?"))
