import os
from typing import Dict, Any, Literal, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class ReflectionDecision(BaseModel):
    decision: Literal["PASS", "SOFTEN", "REJECT"] = Field(description="The verdict on the draft response")
    critique: str = Field(description="Explanation of why the decision was made")
    suggested_revision: Optional[str] = Field(None, description="A revision if decision is SOFTEN")

from backend.utils.model_selector import get_best_flash_model

class ReflectionAgent:
    def __init__(self):
        selected_model = get_best_flash_model()
        self.llm = ChatGoogleGenerativeAI(
            model=selected_model,
            google_api_key=os.getenv("Google_Gemini_Api_Key"),
            temperature=0
        )
        self.structured_llm = self.llm.with_structured_output(ReflectionDecision)

    def review_response(self, draft: str, user_profile: Dict[str, Any]) -> ReflectionDecision:
        """
        Post-Reasoning Gate: Evaluates the draft for safety, tone, and goal alignment.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are the NEEL Reflection Agent. Your job is to audit the Reasoning Agent's draft.
            
            CRITERIA:
            1. REJECT if the draft gives medical, financial, or legal advice.
            2. SOFTEN if the draft is too prescriptive (uses "You must," "You should" too much).
            3. PASS if the draft is analytical, nuanced, and goal-aligned.
            4. REJECT if the draft makes up data that wasn't in the analytics.
            """),
            ("human", "User Goal: {goal}\n\nDraft Response: {draft}")
        ])

        chain = prompt | self.structured_llm
        return chain.invoke({
            "goal": user_profile.get("primary_goal"),
            "draft": draft
        })
