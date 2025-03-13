import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY=os.getenv("API_KEY")


print("|| Type 'exit' to close the chat. ||")
print("How can I assist you today?\n")
while True:
  user = input("> ")
  
  if (user.lower() == 'exit'):
    break
  
  else:
    
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
        {"role": "user", "content": f"{user}"},
    ],
    
  })
)

  response = response.json()

  print('\n\n', response['choices'][0]['message']['content'])