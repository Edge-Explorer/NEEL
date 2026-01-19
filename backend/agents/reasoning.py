import os
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class ReasoningAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("Google_Gemini_Api_Key"),
            temperature=0.7 # Higher temperature for more natural, nuanced guidance
        )

    def generate_guidance(self, user_profile: Dict[str, Any], analytics: Dict[str, Any]) -> str:
        """
        Generates personalized guidance based on user goals and recent behavior.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are NEEL, a highly sophisticated AI Life Coach and Productivity strategist.
            Your goal is to provide deep, non-prescriptive, and cautious reasoning based on data.

            PHILOSOPHY:
            - You do not give generic advice (like "sleep more").
            - You identify success patterns and potential friction points.
            - You speak with nuance (use words like "appears," "might," "suggests").
            - You relate everything back to the user's Primary Goal.

            CONSTRAINTS:
            - Keep your response under 250 words.
            - Focus on the correlation between activities and outcomes.
            - Do not be overly optimistic; be realistic and analytical.
            """),
            ("human", """
            User Primary Goal: {goal}
            User Focus Areas: {focus}
            
            Recent Analytics (Last 7 Days):
            - Total Active Minutes: {total_mins}
            - Activity Distribution: {distribution}
            - Recent Outcomes: {outcomes}

            Provide a reasoning-driven analysis of how the user's current behavior aligns with their goal.
            """)
        ])

        chain = prompt | self.llm | StrOutputParser()
        
        return chain.invoke({
            "goal": user_profile.get("primary_goal"),
            "focus": user_profile.get("focus_areas"),
            "total_mins": analytics.get("total_active_minutes"),
            "distribution": analytics.get("activity_distribution"),
            "outcomes": analytics.get("recent_outcomes")
        })
