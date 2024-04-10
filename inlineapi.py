import google.generativeai as genai
from keys.requests import get_good_key


async def respond(text):
    key = await get_good_key()
    if key == "High load, please wait":
      return key  
    
    genai.configure(api_key=str(key))
    model = genai.GenerativeModel('gemini-pro')
    answer = await model.generate_content_async(text)
    return str(answer.text)
