import google.generativeai as genai

genai.configure(api_key='AIzaSyCzzvmLiQPhl0CHfq3fJYQXEqpGf5JCt4g')

model = genai.GenerativeModel('gemini-pro')


def respond(text):
    return model.generate_content(text)
