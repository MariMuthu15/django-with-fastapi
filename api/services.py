import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in .env file")
        
        self.client = genai.Client(
            api_key=api_key,
            http_options={'api_version': 'v1alpha'}
        )
        self.model_id = 'gemini-flash-latest'
        self.system_instruction = "You are a helpful assistant. Provide your responses in plain text only. Do not use markdown formatting such as bolding (**), italics (_), headers (#), or lists (-). Use simple text structure instead."

    async def get_response(self, prompt: str):
        try:
            # The new SDK also has a synchronous call, we'll run it in a thread.
            import asyncio
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_id,
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    system_instruction=self.system_instruction
                )
            )
            return response.text
        except Exception as e:
            return f"Error communicating with Gemini (new SDK): {str(e)}"

# Singleton instance
gemini_service = GeminiService()
