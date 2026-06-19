import os

from openai import OpenAI
from dotenv import load_dotenv

from app.providers.base_provider import BaseProvider


load_dotenv()


class GroqProvider(BaseProvider):

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv(
                "GROQ_API_KEY"
            ),
            base_url="https://api.groq.com/openai/v1"
        )

    def generate_response(
    self,
    task: str,
    context: str,
    strategy: str
) -> str:

        prompt = f"""
You are an assistant that answers only using the provided context.

Task:
{task}

Context:
{context}

Answer:
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content