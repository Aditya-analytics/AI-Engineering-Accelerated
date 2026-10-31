from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.chat_models import init_chat_model
import asyncio
LOCAL_MODEL_NAME = "gemma4:e4b"
import os 
from dotenv import load_dotenv
load_dotenv()

open_local_model = init_chat_model(
    model="openai/gpt-4o-mini",
    model_provider="openai",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
    streaming=True
)

prompt = ChatPromptTemplate.from_messages(
    [('system','You are a helpful assistant , answer in 2 or 3 sentences'),
    ('user','{question}')]
)

chain = prompt | open_local_model

async def ask_ai(query:str):
    full_response = ""
    async for chunk in chain.astream({"question":query}):
        print(chunk.content, end="", flush=True)

        if chunk.content:
            full_response+=chunk.content
    print()
    return full_response
    


response = asyncio.run(ask_ai("What is the famous dish in india"))

