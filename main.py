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
question = input("ask any technical question: ")
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=question,
    config=types.GenerateContentConfig(
        system_instruction="""You are only able to answer technical questions. Other topics are out of your scope.
        If the question is not technical, respond with "Sorry, I can only answer technical questions.".""",
    )
)
print(response.text)