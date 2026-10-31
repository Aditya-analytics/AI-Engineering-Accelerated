import os
# pyrefly: ignore [missing-import]
from openai import OpenAI
from dotenv import load_dotenv 

# Load environment variables from a .env file
load_dotenv()

# Initialize the OpenAI client pointed at OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Request a completion
completion = client.chat.completions.create(
    model="meta-llama/llama-3.3-70b-instruct",  # You can also use "openai/gpt-4o" or any OpenRouter model string
    messages=[
        {"role": "user", "content": "Complete this sentence in 5 words or less: Life is like a..."}
    ]
)

# Print the response content
print(completion.choices[0].message.content)
