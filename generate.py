from openai import OpenAI

from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Access environment variables
openai_key = os.getenv("OPENAI_API_KEY")

# Uses OPENAI_API_KEY from environment
client = OpenAI(api_key=openai_key)

def generate_answer(system_prompt, user_prompt, model="gpt-4o-mini"):
    """
    Calls the LLM and returns the answer text.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0  # IMPORTANT: factual QA
    )

    return response.choices[0].message.content.strip()
