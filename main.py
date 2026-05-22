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
conversation = []
while(True):
    question = input("ask any technical question: ")
    conversation.append((question, ""))
    if question.lower() == "exit":
        print("Exiting the chatbot. Goodbye!")
        break
    
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=conversation,
        config=types.GenerateContentConfig(
            system_instruction="""You are only able to answer technical questions. Other topics are out of your scope.
            If the question is not technical, respond with "Sorry, I can only answer technical questions.".
            here is the conversation history:
            format is [(question , answer)]""",
        )
    )

    conversation.append((question, response.text))
    print(response.text)
    
