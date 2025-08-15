import os
from dotenv import load_dotenv
import openai

class ChatGPTWrapper:
    def __init__(self, model="gpt-4"):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in env file")
        openai.api_key = api_key
        self.model = model

    def get_chat_response(self, prompt, system_prompt=None, temperature=0.78, max_tokens=500):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {str(e)}"
