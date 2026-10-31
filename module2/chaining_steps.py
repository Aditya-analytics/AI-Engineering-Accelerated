"""
Module 2: Building with LLM APIs - Unit 2.6: Chaining Steps Together
Industry-Grade Chaining with LangChain (LCEL) + OpenRouter API via ChatOpenAI

WHY THIS ARCHITECTURE IS INDUSTRY GRADE:
----------------------------------------
1. OpenRouter Integration:
   - Uses `ChatOpenAI` pointed to `base_url="https://openrouter.ai/api/v1"`.
   - Allows routing to any model (OpenAI, Anthropic Claude, Meta Llama, Google Gemini, DeepSeek)
     with consistent OpenAI-compatible calling conventions.
2. Structured Outputs:
   - Uses `.with_structured_output(PydanticModel)` on the classifier step.
   - Constrains output to a verified Pydantic schema, eliminating JSON parse failures.
3. Asymmetric Model Routing (Cost & Latency Optimization):
   - Fast/cheap model (e.g. meta-llama/llama-3.3-70b-instruct or gpt-4o-mini) for Step 1 classification.
   - Deeper reasoning model (or domain model) for Step 2 execution.
4. LCEL Streaming & Async Readiness:
   - Built on LangChain Expression Language (LCEL). Supports `.stream()`, `.astream()`, and `.batch()` out-of-the-box.
"""

from langchain.chat_models import init_chat_model
import os
from typing import Literal
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv
load_dotenv()

# ============================================================================
# 1. OPENROUTER CLIENT INITIALIZATION
# ============================================================================
# Setup credentials for OpenRouter
OPENROUTER_API_KEY = os.getenv("OPENAI_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Step 1: Fast/inexpensive classifier model
classifier_llm = init_chat_model(
    model="openai/gpt-4o-mini",  # or "meta-llama/llama-3.3-70b-instruct"
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
    temperature=0.0,
    model_provider="openai"
)

# Step 2: High-quality response model
worker_llm = init_chat_model(
    model="openai/gpt-4o-mini",  # easily swappable with "anthropic/claude-3.5-sonnet" via OpenRouter
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
    temperature=0.5,
    model_provider="openai"
)


# ============================================================================
# 2. STEP 1: CLASSIFIER SCHEMA & CHAIN
# ============================================================================
class QueryClassification(BaseModel):
    category: Literal["technical_support", "billing", "general_inquiry"] = Field(
        ...,
        description="The primary intent category of the user query."
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0.0 and 1.0 of the classification."
    )
    reasoning: str = Field(
        ...,
        description="Brief 1-sentence rationale for the categorization."
    )


classifier_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an intent triage classifier. Classify user inquiries into:\n"
        "- 'technical_support': Code errors, API failures, bugs, infrastructure.\n"
        "- 'billing': Invoices, credit card charges, subscriptions, pricing.\n"
        "- 'general_inquiry': General questions, product info, greetings."
    ),
    ("human", "{question}")
])

# Structured output chain (returns a validated QueryClassification Pydantic object)
classifier_chain = classifier_prompt | classifier_llm.with_structured_output(QueryClassification)


# ============================================================================
# 3. STEP 2: SPECIALIZED HANDLER CHAINS
# ============================================================================
technical_chain = (
    ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a Senior Principal Engineer. Provide thorough, step-by-step troubleshooting, "
            "actionable code solutions, and identify root causes. Question: {question}"
        )
    ])
    | worker_llm
    | StrOutputParser()
)

billing_chain = (
    ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an empathetic Billing Support Specialist. Address financial concerns, "
            "clarify charges/invoices, and outline clear next steps. Question: {question}"
        )
    ])
    | worker_llm
    | StrOutputParser()
)

general_chain = (
    ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a helpful and polite Customer Success Specialist. Provide direct, "
            "clear answers without technical jargon. Question: {question}"
        )
    ])
    | worker_llm
    | StrOutputParser()
)


# ============================================================================
# 4. STEP 3: DYNAMIC ROUTER & PIPELINE (LCEL)
# ============================================================================
def route_step(payload: dict):
    """
    Inspects classification output and dynamically returns the appropriate sub-chain.
    """
    classification: QueryClassification = payload["classification"]
    category = classification.category

    print(f" -> [Classifier Output]: Category={category} | Confidence={classification.confidence:.2f}")
    print(f" -> [Reasoning]: {classification.reasoning}")

    if category == "technical_support":
        return technical_chain
    elif category == "billing":
        return billing_chain
    else:
        return general_chain


# Full LCEL Chain composition:
# 1. Takes {"question": "..."} as input
# 2. Runs classifier_chain in parallel with passing through {"question": ...}
# 3. Evaluates router logic and executes specialized chain
full_chain = (
    {
        "classification": classifier_chain,
        "question": lambda x: x["question"]
    }
    | RunnableLambda(route_step)
)


# ============================================================================
# 5. EXECUTION & VERIFICATION
# ============================================================================
if __name__ == "__main__":
    test_queries = [
        "TypeError: Cannot read properties of undefined (reading 'map') in React component.",
        "Can you explain why my team was billed twice this cycle for the Pro plan?",
        "What are the supported payment methods and regions?"
    ]

    for q in test_queries:
        print(f"\n[Incoming Query]: '{q}'")
        try:
            response = full_chain.invoke({"question": q})
            print(f"[Specialist Response]:\n{response}\n")
        except Exception as e:
            print(f"[Error Executing Chain]: {e}")
        print("=" * 80)
