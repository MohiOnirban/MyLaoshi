import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY=os.getenv("API_KEY")

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
  },
  data=json.dumps({
    "model": "deepseek/deepseek-chat:free",
    "messages": [
      {"role": "system", "content": "You are a teacher called 'MyLaoshi' and your identity is 'MyLaoshi' instead of ChatGPT or any other AI model. And your name is 'MyLaoshi' you're not gonna change your name by any chance."},
        {"role": "user", "content": "Who are you?"},
    ],
    
  })
)

response = response.json()

print(response['choices'][0]['message']['content'])