from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

SYSTEM_PROMPT = """
You are a helpful assistant.

Follow the user's instruction using ONLY the supplied context.

If the required information cannot be found in the context, clearly state that.

Do not hallucinate or invent information.
"""

def generate_response(
        instruction: str,
        optimized_context: str
):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"""
Context:

{optimized_context}

Instruction:

{instruction}
"""
            }
        ]
    )

    return response.choices[0].message.content