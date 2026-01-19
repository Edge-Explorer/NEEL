import os
from typing import Dict, Any, Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class ConfidenceScore(BaseModel):
    confidence: Literal["LOW", "MEDIUM", "HIGH"] = Field(description="Confidence level in the data sufficiency")
    reason: str = Field(description="Explanation for the assigned confidence level")
    allow_reasoning: bool = Field(description="Whether the LLM is allowed to give advice")

class SupervisorAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("Google_Gemini_Api_Key"),
            temperature=0
        )
        self.structured_llm = self.llm.with_structured_output(ConfidenceScore)

    def evaluate_data(self, user_profile: Dict[str, Any], analytics: Dict[str, Any]) -> ConfidenceScore:
        """
        Gated evaluation: Determines if the data is sufficient for reasoning.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are the NEEL Supervisor Agent. Your role is NOT to provide advice, but to act as a security gate.
            You must evaluate if the user's logged activity is stable enough to draw conclusions.

            RULES:
            - If total_active_minutes < 120 (for 7 days), confidence is LOW.
            - If there are no outcomes (results) linked to logs, confidence is MEDIUM.
            - If the user has a primary goal but no matching activity logs, allow_reasoning must be FALSE.
            """),
            ("human", "User Profile: {profile}\n\nRecent Analytics: {analytics}")
        ])

        chain = prompt | self.structured_llm
        return chain.invoke({"profile": user_profile, "analytics": analytics})
