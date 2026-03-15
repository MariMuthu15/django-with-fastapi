import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in .env file")
        
        genai.configure(api_key=api_key)
        self.model_name = 'models/gemini-flash-lite-latest'
        self.system_instruction = "You are a helpful assistant. Provide concise and accurate responses using markdown formatting where appropriate."
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=self.system_instruction
        )

    async def get_response(self, prompt: str):
        try:
            import asyncio
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt
            )
            return response.text
        except Exception as e:
            return f"Error communicating with Gemini: {str(e)}"

# Singleton instance
gemini_service = GeminiService()
