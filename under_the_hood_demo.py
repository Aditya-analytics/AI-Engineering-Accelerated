"""
=============================================================================
UNDER THE HOOD: How LangChain Handles Failures & Self-Healing
=============================================================================
This script demonstrates step-by-step with print statements:
1. What happens when raw LLM output is broken (BaseParser fails).
2. The EXACT secret prompt LangChain sends behind the scenes to fix it.
3. How OutputFixingParser repairs the broken output.
4. What happens if the model KEEPS FAILING (Attempt 2 fails), and how
   fallback prevents an infinite loop or crash!
=============================================================================
"""

import sys
import os
import json
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain.output_parsers import OutputFixingParser
from langchain.output_parsers.fix import NAIVE_FIX_PROMPT
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.exceptions import OutputParserException
from langchain_core.runnables import RunnableLambda

# =====================================================================
# 1. DEFINE OUR SCHEMA BLUEPRINT
# =====================================================================
class UserProfile(BaseModel):
    name: str = Field(description="User's full name")
    age: int = Field(description="User's age in years")
    role: str = Field(description="User's role: 'admin' or 'member'")

base_parser = PydanticOutputParser(pydantic_object=UserProfile)


def print_banner(title: str):
    print("\n" + "=" * 75)
    print(f"  {title}")
    print("=" * 75)


# =====================================================================
# SCENARIO 1: The "Toy" Way (Base Parser crashes immediately)
# =====================================================================
print_banner("SCENARIO 1: What happens with standard BaseParser on broken output")

# Simulate a typical bad LLM output (missing quotes, string instead of int for age)
broken_llm_output = """
```json
{
    name: "Alex",
    "age": "twenty-five",
    "role": "admin"
}
```
"""

print("[Input from LLM]:")
print(broken_llm_output.strip())

print("\n[Action]: Calling base_parser.parse()...")
try:
    base_parser.parse(broken_llm_output)
    print("✅ Parsed successfully!")
except Exception as e:
    print("❌ BASE PARSER CRASHED!")
    print(f"   Error Type: {type(e).__name__}")
    print(f"   Error Reason: {str(e)[:180]}...")


# =====================================================================
# SCENARIO 2: Peek Under the Hood at LangChain's Secret Repair Prompt
# =====================================================================
print_banner("SCENARIO 2: What LangChain's OutputFixingParser does under the hood")

print("When base_parser fails, LangChain doesn't give up.")
print("It dynamically builds a special 'Fixer Prompt' using NAIVE_FIX_PROMPT.\n")

# Format the exact prompt LangChain builds internally
sample_instructions = base_parser.get_format_instructions()
sample_error = "Invalid JSON or schema validation error: Input should be a valid integer for field 'age'."

actual_repair_prompt = NAIVE_FIX_PROMPT.format(
    instructions=sample_instructions,
    completion=broken_llm_output.strip(),
    error=sample_error
)

print("--- [The Exact Internal Prompt Sent to the Repair Model] ---")
print(actual_repair_prompt)
print("------------------------------------------------------------")


# =====================================================================
# SCENARIO 3: Successful Auto-Repair (Attempt 2)
# =====================================================================
print_banner("SCENARIO 3: OutputFixingParser in action (Auto-Repair)")

# We simulate a repair LLM that receives the prompt above and fixes the JSON:
simulated_repair_response = '{"name": "Alex", "age": 25, "role": "admin"}'

repair_llm = FakeListChatModel(responses=[simulated_repair_response])
fixing_parser = OutputFixingParser.from_llm(parser=base_parser, llm=repair_llm)

print("[Step 1]: Sending broken output to fixing_parser...")
repaired_result = fixing_parser.parse(broken_llm_output)

print("\n✅ [Step 2]: OutputFixingParser successfully repaired it!")
print(f"   Parsed Object: {repaired_result}")
print(f"   Type of age: {type(repaired_result.age)} (Converted 'twenty-five' -> integer {repaired_result.age}!)")


# =====================================================================
# SCENARIO 4: What if the model KEEPS FAILING? (Infinite loop prevention)
# =====================================================================
print_banner("SCENARIO 4: What if Attempt 2 ALSO fails? (Does it loop infinitely?)")

# Simulate a model that returns total gibberish on Attempt 2
stubborn_broken_response = "Sorry, I am just an AI and cannot produce JSON for this input."
stubborn_llm = FakeListChatModel(responses=[stubborn_broken_response])
failing_fixer = OutputFixingParser.from_llm(parser=base_parser, llm=stubborn_llm)

print("[Question]: Will it retry infinitely?")
print("[Answer]: NO! It only tries ONCE. Let's see what happens when Attempt 2 fails:\n")

try:
    failing_fixer.parse("Total garbage input that cannot be parsed")
except OutputParserException as err:
    print("🛑 [STOPPED]: OutputFixingParser threw OutputParserException after 1 retry.")
    print("   It refuses to loop infinitely and waste your budget!\n")


# =====================================================================
# SCENARIO 5: The Production Fix (Graceful Degradation Fallback)
# =====================================================================
print_banner("SCENARIO 5: The Senior Engineer Safety Net (Fallbacks)")

print("To prevent the entire web app or API from crashing when parsing fails,")
print("we attach a safe fallback using .with_fallbacks([safe_default]):\n")

def safe_default_user(error_input) -> UserProfile:
    print("   🛡️ [FALLBACK TRIGGERED]: Model failed all attempts.")
    print("   🛡️ Returning safe default profile so the app never throws 500!")
    return UserProfile(name="Guest User", age=0, role="member")

# Chain with fallback
bulletproof_chain = failing_fixer.with_fallbacks([RunnableLambda(safe_default_user)])

# Run with completely impossible input
final_output = bulletproof_chain.invoke("Impossible input $$$###@@@")

print("\n🎉 Final Output received safely by the application:")
print(f"   {final_output}")
print("=" * 75 + "\n")

