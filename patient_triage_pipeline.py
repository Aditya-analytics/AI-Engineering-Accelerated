"""
=============================================================================
HANDS-ON LAB: Resilient AI Medical Triage Pipeline
=============================================================================
YOUR GOAL:
Build an end-to-end, production-grade LangChain pipeline that processes
unstructured patient symptom reports.

REQUIREMENTS:
1. SCHEMA (Pydantic):
   - patient_id: str
   - priority_level: Literal["LOW", "MEDIUM", "EMERGENCY"]
   - symptoms: list[str]
   - recommended_action: str

2. RESILIENT MODEL PIPELINE:
   - Primary model with strict timeout (e.g. 5.0 seconds) and max_retries.
   - Backup model chained via .with_fallbacks([...]).
   (Tip: You can use FakeListChatModel or ChatOpenAI/ChatAnthropic).

3. SELF-HEALING OUTPUT PARSER:
   - Base PydanticOutputParser.
   - Wrapped with OutputFixingParser to repair broken syntax or invalid Literals.

4. FAIL-SECURE GRACEFUL DEGRADATION:
   - If BOTH models fail OR input is unparseable gibberish, your pipeline
     MUST NOT crash with an unhandled exception.
   - Attach a fallback using .with_fallbacks([RunnableLambda(...)]) returning
     a safe emergency default:
     (priority_level="EMERGENCY", recommended_action="Call 911 / Immediate ER")

5. VERIFICATION:
   - Test Case 1: Valid input -> Parses cleanly.
   - Test Case 2: Broken output (e.g. priority_level="SUPER_BAD") -> Auto-repaired.
   - Test Case 3: Complete failure / gibberish -> Gracefully falls back to EMERGENCY.
=============================================================================
"""

# START CODING BELOW:


