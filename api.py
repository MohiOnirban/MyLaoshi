import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

# Initialize the conversation with the system message
conversation = [
    {"role": "system", "content": "You are a teacher called 'MyLaoshi' and your identity is 'MyLaoshi' instead of ChatGPT or any other AI model. And your name is 'MyLaoshi' you're not gonna change your name by any chance."}
]

# Show the initial prompt only once
print("How can I assist you today? (or type 'exit' to quit)")

while True:
    # Empty input prompt for subsequent interactions
    user_input = input("> ")
    
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break
    
    # Add the user's message to the conversation
    conversation.append({"role": "user", "content": user_input})
    
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "deepseek/deepseek-chat:free",
            "messages": conversation,
        })
    )
    
    response = response.json()
    
    # Get the AI's reply
    ai_reply = response['choices'][0]['message']['content']
    
    # Print the AI's reply
    print(f"MyLaoshi: {ai_reply}")
    
    # Add the AI's reply to the conversation
    conversation.append({"role": "assistant", "content": ai_reply})