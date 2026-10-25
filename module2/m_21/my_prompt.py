from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

import os
from dotenv import load_dotenv
load_dotenv()

llm = init_chat_model("openai/gpt-4o-mini",model_provider="openai",base_url="https://openrouter.ai/api/v1")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder("chat_history"),
    ("user", "{question}"),
    ])

chain = prompt | llm 

chat_history = {}
def conv_hist(session_id:str):
    if session_id not in chat_history:
        chat_history[session_id] = []
        
    return chat_history[session_id]
    

def ask_ai(user_input:str,session_id: str, k:int = 2):
    history = conv_hist(session_id)
    response = chain.invoke({
        "chat_history":history[-(k+1):],
        "question":user_input
    })

    ai_response = response.content
    add_content = [{"role": "user", "content": user_input} ,{"role": "assistant", "content": ai_response}]
    chat_history[session_id].extend(add_content)

    return ai_response

# Add these at the bottom to test
print(ask_ai("Hi, my name is Aditya and I love chess.", session_id="u1"))
print(ask_ai("What's my name?", session_id="u1"))
print(ask_ai("What game do I love?", session_id="u1"))
# Now test forgetting — new session with no history
print(ask_ai("What's my name?", session_id="u2"))




   


