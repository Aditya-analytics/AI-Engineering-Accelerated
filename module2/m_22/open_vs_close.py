import time
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# ==========================================
# 1. Closed/Commercial Model (via API)
# ==========================================
# Using the same provider pattern from Module 2.1 (OpenRouter / OpenAI)
closed_llm = init_chat_model(
    model="openai/gpt-4o-mini",
    model_provider="openai",
    base_url=os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1"),
    api_key=os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY"),
)

# ==========================================
# 2. Open Local Model (Ollama via OpenAI API compatibility)
# ==========================================
# Ollama runs an OpenAI-compatible server at http://localhost:11434/v1
# We can use init_chat_model with model_provider="openai"
# without needing extra third-party libraries.
LOCAL_MODEL_NAME = "gemma4:e4b"

open_local_llm = init_chat_model(
    model=LOCAL_MODEL_NAME,
    model_provider="openai",
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # dummy key required by client
)

# Shared prompt template for fair side-by-side comparison
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a concise AI assistant. Answer in 2-3 sentences."),
    ("user", "{question}"),
])

closed_chain = prompt | closed_llm
open_chain = prompt | open_local_llm


def benchmark_model(chain_name: str, chain, question: str):
    print(f"\n--- Running: {chain_name} ---")
    start_time = time.perf_counter()
    try:
        response = chain.invoke({"question": question})
        duration = time.perf_counter() - start_time
        print(f"Response:\n{response.content}")
        print(f"Latency: {duration:.2f}s")
        return response.content, duration
    except Exception as e:
        print(f"Error calling {chain_name}: {e}")
        return None, None


if __name__ == "__main__":
    test_question = "What is parameter quantization in Large Language Models and why is it important?"

    print(f"Comparing Closed Model (gpt-4o-mini) vs Open Local Model ({LOCAL_MODEL_NAME})")
    print(f"Question: {test_question}")

    # 1. Test Open Local Model
    benchmark_model(f"Open Local ({LOCAL_MODEL_NAME})", open_chain, test_question)

    # 2. Test Closed Commercial Model
    benchmark_model("Closed API (gpt-4o-mini)", closed_chain, test_question)
