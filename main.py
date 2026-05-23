from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    print("Error: GENAI_API_KEY not set. Copy .env.example to .env and set your key or set the environment variable.")
    raise SystemExit(1)

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.5-flash"
MAX_TURNS = 6 # why 6? any specific reason?
DEBUG = True

history = []

def debug_log(message):
    if DEBUG:
        print(f"[debug] {message}")

def trim_history(items, max_turns): # what exactly is this function doing? can you explain the logic behind it with example?
    max_items = max_turns * 2
    debug_log(f"Trim check: items={len(items)}, max_items={max_items}")
    if len(items) > max_items:
        debug_log("Trimming history to most recent items")
        return items[-max_items:]
    return items

while True:
    question = input("ask any technical question: ")
    if question.lower() == "exit":
        print("Exiting the chatbot. Goodbye!")
        break

    debug_log("Appending user message to history")
    history.append({"role": "user", "parts": [{"text": question}]})
    history = trim_history(history, MAX_TURNS)
    debug_log(f"History length after user append: {len(history)}, history={history}")

    debug_log("Calling model with current history")
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=history,
        config=types.GenerateContentConfig(
            system_instruction=(
                "You only answer technical questions. If a question is not technical, reply: "
                "Sorry, I can only answer technical questions."
            ),
        ),
    )

    answer = response.text or "" # this is only for the safety if the response is exactly not a string or llm did not return anything then for a safety net we are assigning a empty string? am i exactly right? or is there any other reason for this?
    debug_log("Appending model response to history")
    history.append({"role": "model", "parts": [{"text": answer}]})
    history = trim_history(history, MAX_TURNS)
    debug_log(f"History length after model append: {len(history)}, history={history}")
    print(answer)
    # lastly why this specific format for the history ({"role": "model", "parts": [{"text": answer}]})? is it some specific format that the model expects or is it just a convention we are following here?
    
