from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

class Gemini_client:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API"))
        self.chat = self.client.chats.create(model = "gemini-2.5-pro")

    def generate_content(self, prompt: str):
        response = self.client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt
        )
        
        return response.text
    
    def responses_experiment_2(self, prompt: str):
        response = self.chat.send_message(prompt)
        return response