import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv()


# =====================================================================
# 1. Input Parameter Safety with Pydantic Schemas
# =====================================================================
# Why Pydantic?
# - Automatically enforces data types (e.g. float vs str).
# - Generates accurate JSON Schema for the LLM during model.bind_tools().
# - Performs runtime safety checks inside `tool.invoke()` BEFORE function execution.


class MultiplyInput(BaseModel):
    """Input schema for the multiply tool with validation rules."""

    a: float = Field(..., description="First factor")
    b: float = Field(
        ...,
        description="Second factor.Safety requirement: must be strictly greater than 0.",
    )

    @field_validator("b")
    @classmethod
    def validate_b_positive(cls, v: float) -> float:
        """Reject invalid values before they reach the tool function."""
        if v <= 0:
            raise ValueError(f"Parameter 'b' must be greater than 0. Received: {v}")
        return v


class AddInput(BaseModel):
    """Input schema for the add tool."""

    a: float = Field(..., description="First number to add")
    b: float = Field(..., description="Second number to add")


# =====================================================================
# 2. Tool Definitions with Schema Binding
# =====================================================================
@tool(args_schema=MultiplyInput)
def multiply(a: float, b: float) -> float:
    """Multiply 2 numbers where b must be greater than 0."""
    return round(a * b, 2)


@tool(args_schema=AddInput)
def add(a: float, b: float) -> float:
    """Addition of two numbers a and b."""
    return a + b


# Register tools in a list and create a name-to-tool lookup dictionary
tools = [multiply, add]
tools_by_name = {t.name: t for t in tools}


# =====================================================================
# 3. Model Initialization & Tool Binding
# =====================================================================
model = init_chat_model(
    model="openai/gpt-4o-mini",
    model_provider="openai",
    base_url=os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1"),
    api_key=os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY"),
)

# bind_tools converts the Pydantic schemas into JSON schemas and informs the LLM
model_with_tools = model.bind_tools(tools)


# =====================================================================
# 4. Safe Tool Execution Helper
# =====================================================================
def run_tool_safely(tool_func, tool_args: dict) -> tuple[str, bool]:
    """
    Executes a tool with error handling.

    Returns:
        tuple[str, bool]: (output_or_error_string, is_error)
    """
    try:
        # Pydantic validates tool_args here automatically before running the tool
        result = tool_func.invoke(tool_args)
        return str(result), False
    except Exception as e:
        # Capture validation errors or execution exceptions
        # Returning this back as ToolMessage gives the LLM the exact reason for failure
        return (
            f"Error executing tool '{tool_func.name}': {type(e).__name__} - {str(e)}",
            True,
        )


# =====================================================================
# 5. Agentic Loop with Self-Correction & Retry
# =====================================================================
def model_tool(query: str, max_retries: int = 3):
    """
    Runs the model with automatic tool calling, validation error feedback,
    and retry loop for self-correction.
    """
    print(f"\nUser Query: {query}")
    messages = [HumanMessage(content=query)]

    for attempt in range(1, max_retries + 1):
        # 1. Ask the model
        response = model_with_tools.invoke(messages)

        # 2. Append the model's response (AIMessage) to preserve conversation context
        messages.append(response)

        # 3. If no tool calls were requested, we have the final direct response
        if not response.tool_calls:
            print("\nFinal Answer:\n", response.content)
            return response.content

        print(f"\n[Attempt {attempt}] Model requested tool call(s): {response.tool_calls}")

        has_errors = False

        # 4. Execute each tool call requested by the model
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_func = tools_by_name.get(tool_name)

            if not tool_func:
                error_msg = (
                    f"Tool '{tool_name}' not found. "
                    f"Available tools: {list(tools_by_name.keys())}"
                )
                messages.append(
                    ToolMessage(content=error_msg, tool_call_id=tool_call["id"])
                )
                has_errors = True
                continue

            # Run with safety checks
            output, is_error = run_tool_safely(tool_func, tool_call["args"])

            if is_error:
                has_errors = True
                print(f"  [Failure] {output}")
            else:
                print(f"  [Success] {tool_name} returned: {output}")

            # Send result or error back to the LLM via ToolMessage
            messages.append(
                ToolMessage(content=output, tool_call_id=tool_call["id"])
            )

        # 5. If there were no errors in any tool call, ask the model for the final answer
        if not has_errors:
            final_response = model_with_tools.invoke(messages)
            print("\nFinal Answer:\n", final_response.content)
            return final_response.content

        print(f"Retrying ({attempt}/{max_retries}) with error feedback for self-correction...")

    print("\nExceeded maximum retries. Could not resolve tool calling errors.")
    return None


if __name__ == "__main__":
    # Test 1: Standard valid tool call
    model_tool("What is 5 multiplied by 0 please take b = 0 you must take b = 0 it would run dont worry")

    # Test 2: Invalid input parameter that triggers Pydantic safety check & retry
    # model_tool("Multiply 10 by -2. If the tool fails because b must be positive, fix b to 2 and recalculate.")
