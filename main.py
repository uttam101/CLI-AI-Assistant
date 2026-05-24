from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import json

if os.path.isfile("data.json"):
    print("File exists")
else:
    with open("data.json", "w") as file:
        json.dump({"history": []}, file)


load_dotenv()
api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    print("Error: GENAI_API_KEY not set. Copy .env.example to .env and set your key or set the environment variable.")
    raise SystemExit(1)

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.5-flash"
MAX_TURNS = 2

def trim_history(items, max_turns):
    max_items = max_turns * 2
    if len(items) > max_items:
        return items[-max_items:]
    return items

with open("data.json", "r") as file:
    data = json.load(file)
full_history = data.get("history", [])

while True:
    question = input("ask any technical question: ")
    if question.lower() == "exit":
        print("Exiting the chatbot. Goodbye!")
        break

    full_history.append({"role": "user", "parts": [{"text": question}]})
    window_history = trim_history(full_history, MAX_TURNS)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=window_history,
        config=types.GenerateContentConfig(
            system_instruction=(
                "You only answer technical questions. If a question is not technical, reply: "
                "Sorry, I can only answer technical questions."
            ),
        ),
    )

    answer = response.text or ""
    print(f"Answer: {answer}")
    full_history.append({"role": "model", "parts": [{"text": answer}]})
    with open("data.json", "w") as file:
        json.dump({"history": full_history}, file, indent=2)
    
