import requests
import json
import os
import sqlite3
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket
from typing import List

# Load API Key
load_dotenv()
API_KEY = os.getenv("API_KEY")

# SQLite Database Setup
conn = sqlite3.connect("student_progress.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS progress
                 (id INTEGER PRIMARY KEY, student_name TEXT, subject TEXT, question TEXT, answer TEXT, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

# Subject Selection
subjects = ["Math", "Physics", "Psychology", "Chinese Culture"]
print("Choose a subject: ")
for i, subject in enumerate(subjects, 1):
    print(f"{i}. {subject}")

subject_choice = input("> ")
selected_subject = subjects[int(subject_choice) - 1]

system_prompt = f"You are a mentor called 'MyLaoshi'. You specialize in {selected_subject}. Your job is to guide students step by step without directly solving their problems. If a student is struggling, give hints first before revealing the full answer."

# Function to save progress
def save_progress(student_name, subject, question, answer):
    cursor.execute("INSERT INTO progress (student_name, subject, question, answer) VALUES (?, ?, ?, ?)", 
                   (student_name, subject, question, answer))
    conn.commit()

# Function to get chapter overview
def get_chapter_overview():
    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Give me a short overview of the {selected_subject} chapter before we start learning."}]

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        data=json.dumps({"model": "deepseek/deepseek-chat:free", "messages": messages})
    )

    return response.json()['choices'][0]['message']['content']

# Display Chapter Overview
print("\nChapter Overview:\n", get_chapter_overview())

# Chatbot Loop
print("\n|| Type 'exit' to close the chat. ||")
print("How can I assist you today?\n")

while True:
    user = input("> ")
    
    if user.lower() == 'exit':
        break

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"{user}"}
    ]

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        data=json.dumps({"model": "deepseek/deepseek-chat:free", "messages": messages})
    )

    assistant_response = response.json()['choices'][0]['message']['content']
    print("\nHint: ", assistant_response)

    follow_up = input("\nDid that help? (yes/no): ")

    if follow_up.lower() == "no":
        messages.append({"role": "user", "content": "I still don't understand. Can you explain more?"})

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            data=json.dumps({"model": "deepseek/deepseek-chat:free", "messages": messages})
        )

        assistant_response = response.json()['choices'][0]['message']['content']
        print("\nFull Answer: ", assistant_response)

    # Save progress
    student_name = input("\nEnter your name for progress tracking: ")
    save_progress(student_name, selected_subject, user, assistant_response)

conn.close()
