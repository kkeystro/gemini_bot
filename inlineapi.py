import google.generativeai as genai
from keys.requests import get_good_key


async def gkey():
    key = await get_good_key()
    return key


async def respond(text):
    genai.configure(api_key=str(await gkey()))
    model = genai.GenerativeModel('gemini-pro')
    return model.generate_content(text)
