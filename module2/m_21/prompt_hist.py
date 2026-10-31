import os
from dotenv import load_dotenv
from langchain_core.messages import convert_to_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

load_dotenv()
OPEN_ROUTER = os.getenv("OPENROUTER_API_KEY")

# 1. Initialize LangChain model
llm = ChatOpenAI(
    model="openai/gpt-4o-mini",  # or any model on OpenRouter
    api_key=OPEN_ROUTER,  # your OpenRouter key
    base_url="https://openrouter.ai/api/v1",
)

# 2. Build the template with a placeholder for the history block
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history_window"),  # Manual past turns go here
        ("human", "{user_input}"),  # Live dynamic input goes here
    ]
)

# Create the pipeline chain
chain = prompt_template | llm

# Global nested list store: [[session_id, [message_history_list]], ...]
session_list_store = []


def get_or_create_history(session_id: str):
    # FIXED: Check the first element of the item sublist, and return the second element
    for item in session_list_store:
        if item[0] == session_id:
            return item[1]

    # We start with an empty array because the system prompt is already handled by ChatPromptTemplate
    initial_history = []
    session_list_store.append([session_id, initial_history])
    return initial_history


def chat_with_prompt_and_history(user_input: str, session_id: str, k: int = 2) -> str:
    """Uses ChatPromptTemplate and LangChain to execute the run,

    while keeping the history state and K-truncation completely manual.
    """
    # Fetch the manual history list (list of dicts)
    full_history = get_or_create_history(session_id)

    # Apply manual "Last K History" window truncation on the dict list
    truncated_dict_history = full_history[-k:]

    # Convert the manual dicts into LangChain message objects so the prompt template can read them
    langchain_history_window = convert_to_messages(truncated_dict_history)

    # Invoke the chain, injecting the formatted history and the dynamic user input
    response = chain.invoke(
        {"history_window": langchain_history_window, "user_input": user_input}
    )

    ai_response = response.content

    # Append this complete turn to your manual persistent track for the next loop
    full_history.append({"role": "user", "content": user_input})
    full_history.append({"role": "assistant", "content": ai_response})

    return ai_response


# --- Example Usage ---

# Turn 1: History window sent to model = []
reply1 = chat_with_prompt_and_history(
    "Hi, I bought a new guitar today.", session_id="user_abc"
)
print("AI Turn 1:", reply1)

# Turn 2: History window sent to model = [User: Guitar, AI: Turn 1 Reply]
reply2 = chat_with_prompt_and_history(
    "What instrument did I get?", session_id="user_abc"
)
print("AI Turn 2:", reply2)

# Turn 3: History window sent to model = [User: What instrument?, AI: Turn 2 Reply]
# Note: The guitar info from Turn 1 falls out of the `k=2` window here, but Turn 2 still implicitly contains it!
reply3 = chat_with_prompt_and_history(
    "Also, my favorite food is sushi.", session_id="user_abc"
)
print("AI Turn 3:", reply3)

# Turn 4: History window sent to model = [User: Favorite food is sushi, AI: Turn 3 Reply]
# The model completely forgets! It has no context remaining about guitars or instruments.
reply4 = chat_with_prompt_and_history(
    "What instrument did I buy again?", session_id="user_abc"
)
print("AI Turn 4:", reply4)
