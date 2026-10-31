from typing import List
from pydantic import BaseModel, Field, field_validator
from pydantic import ValidationError
import re
import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

class Receipt(BaseModel):
    name: str = Field(description="Full name of the customer or buyer")
    date: str = Field(description="Date of the transaction or purchase")
    amount: str = Field(description="Total amount paid including currency symbol if present")
    category: str = Field(description="Category of the purchase e.g. Groceries, Electronics, Travel etc.")

    @field_validator("name")
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("name cannot be empty")
        return v.strip()

    @field_validator("amount")
    def amount_has_value(cls, v):
        if not re.search(r"\d", v):
            raise ValueError(f"amount '{v}' has no numeric value")
        return v

    # @field_validator("category")
    # def category_is_known(cls, v):
    #     known = {"groceries", "electronics", "restaurant", "travel", "health",
    #              "utilities", "education", "clothing", "furniture", "subscription"}
    #     if v.lower() not in known:
    #         raise ValueError(f"Unknown category: {v}")
    #     return v

class Extract(BaseModel):
    data: List[Receipt] = Field(description="List of all extracted receipts")

class GetContent:
    def __init__(self, path):
        self.file_path = path

    def get_content(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return f.read()
        else:
            print(f"File path {self.file_path} doesn't exist")

class LLM:
    def __init__(self, path, max_retries=3):
        self.model = init_chat_model(
            model="openai/gpt-4o-mini",
            model_provider="openai",
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.structured_model = self.model.with_structured_output(Extract, include_raw=True)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Extract name, date, amount and category from 10 messy text receipts"),
            ("user", "{data}")
        ])
        self.path = path
        self.max_retries = max_retries

    def get_data(self):
        content = GetContent(path=self.path).get_content()
        chain = self.prompt | self.structured_model

        for attempt in range(1, self.max_retries + 1):
            print(f"Attempt {attempt}/{self.max_retries}...")
            try:
                raw = chain.invoke({"data": content})

                if raw["parsing_error"]:
                    print(f"  ❌ Parsing error: {raw['parsing_error']} — retrying...")
                    continue

                result: Extract = raw["parsed"]

                if len(result.data) == 0:
                    print("  ❌ No receipts extracted — retrying...")
                    continue

                print(f"  ✅ Success! Extracted {len(result.data)} receipts.")
                return result

            except ValidationError as e:
                print(f"  ❌ Validation Error on attempt {attempt}: {e}")
            except Exception as e:
                print(f"  ❌ LLM/API Error on attempt {attempt}: {e}")

        print("⛔ Max retries reached. Could not extract valid data.")
        return None


ob1 = LLM("/Users/macsuyash4/Downloads/ai-mentor/module2/reciept.txt", max_retries=3)
result = ob1.get_data()

if result:
    for i, receipt in enumerate(result.data, 1):
        print(f"Receipt {i}: Name={receipt.name} | Date={receipt.date} | Amount={receipt.amount} | Category={receipt.category}")
