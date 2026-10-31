import os
import requests
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool

load_dotenv()


@tool
def get_current_weather(latitude: float, longitude: float) -> float:
    """Fetch current temperature via Open-Meteo API.

    Inputs:  latitude, longitude (floats)
    Returns: Current temperature in °C (float)
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m",
    }
    data = requests.get(url, params=params, timeout=10).json()
    temp = float(data["current"]["temperature_2m"])
    print(f"Current temp: {temp}°C (type: {type(temp).__name__})")
    return temp


@tool
def get_currency(target_currency: str, base_code: str = "USD") -> str:
    """Get exchange rate for target currency relative to base currency.

    :param target_currency: Currency code to convert to (e.g., 'EUR', 'INR').
    :param base_code: Base currency code (default: 'USD').
    :return: Exchange rate as a string.
    """
    url = f"https://open.er-api.com/v6/latest/{base_code.upper()}"
    response = requests.get(url, timeout=10)
    data = response.json()["rates"]
    return str(data[target_currency.upper()])


tools = [get_current_weather, get_currency]
tools_by_name = {t.name: t for t in tools}

model = init_chat_model(
    model="openai/gpt-4o-mini",
    model_provider="openai",
    base_url=os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1"),
    api_key=os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY"),
)

# bind_tools converts the functions into JSON schemas and informs the LLM
model_with_tools = model.bind_tools(tools)


def ask_ai(query: str) -> str:
    messages = [
        SystemMessage(content="You are a helpful assistant which uses proper tools if needed."),
        HumanMessage(content=query),
    ]
    response = model_with_tools.invoke(messages)
    messages.append(response)

    if not response.tool_calls:
        print("Final answer:", response.content)
        return response.content

    print(f"\n[Tool Calls Detected: {len(response.tool_calls)}]")
    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_id = tool_call["id"]
        print(f" -> Calling Tool: '{tool_name}' (ID: {tool_id}) with args: {tool_args}")

        tool_func = tools_by_name.get(tool_name)
        if not tool_func:
            tool_result = f"Error: Tool '{tool_name}' not found."
        else:
            tool_result = tool_func.invoke(tool_args)

        print(f" <- Tool Result: {tool_result}")
        messages.append(
            ToolMessage(content=str(tool_result), tool_call_id=tool_id)
        )

    final_response = model.invoke(messages)
    return final_response.content


if __name__ == "__main__":
    test_queries = [
        # Test 1: No tool needed
        "What is the capital of France?",
        # Test 2: Weather tool test
        "What is the current temperature in India?",
        # Test 3: Currency tool test
        "What is the exchange rate of 1 USD to INR?",
        # Test 4: Multi-tool test
        "What is the weather in USA  and what is 10 USD to JPY?",
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*20} Test {i} {'='*20}")
        print(f"User: {query}")
        answer = ask_ai(query)
        print(f"AI:   {answer}")
