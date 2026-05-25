from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import json
import argparse

DATA_FILE = "data.json"
MODEL_NAME = "gemini-3.5-flash"
MAX_TURNS = 2

def parse_args():
    parser = argparse.ArgumentParser(description="Script to add command-line arguments")
    parser.add_argument("--reset", action="store_true", help="Reset the conversation history")
    parser.add_argument("--persona", type=str, default="technical assistant", help="set a persona for the chatbot")
    return parser.parse_args()

def init_storage(reset_history):
    if os.path.isfile(DATA_FILE):
        if reset_history:
            write_history([])
    else:
        write_history([])

def load_history():
    with open(DATA_FILE, "r") as file:
        data = json.load(file)
    return data.get("history", [])

def write_history(history):
    with open(DATA_FILE, "w") as file:
        json.dump({"history": history}, file, indent=2)

def get_api_key():
    load_dotenv()
    api_key = os.getenv("GENAI_API_KEY")
    if not api_key:
        print("Error: GENAI_API_KEY not set. Copy .env.example to .env and set your key or set the environment variable.")
        raise SystemExit(1)
    return api_key

def build_client():
    api_key = get_api_key()
    return genai.Client(api_key=api_key)

def trim_history(items, max_turns):
    max_items = max_turns * 2
    if len(items) > max_items:
        return items[-max_items:]
    return items

def run_chat(client, full_history, persona):
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
                    f"You are a {persona}. Answer technical questions clearly and concisely. "
                    "If a question is not technical, reply politely that it is out of scope for a technical assistant."
                ),
            ),
        )

        answer = response.text or ""
        print(f"Answer: {answer}")
        full_history.append({"role": "model", "parts": [{"text": answer}]})
        write_history(full_history)

def main():
    args = parse_args()
    init_storage(args.reset)
    client = build_client()
    full_history = load_history()
    run_chat(client, full_history, args.persona)

if __name__ == "__main__":
    main()