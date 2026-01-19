import os
from typing import Dict, Any, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class ReasoningAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("Google_Gemini_Api_Key"),
            temperature=0.7 # Higher temperature for more natural, nuanced guidance
        )

    def generate_guidance(self, user_profile: Dict[str, Any], analytics: Dict[str, Any], historical_summaries: List[Dict[str, Any]] = None) -> str:
        """
        Generates personalized guidance based on user goals, recent behavior, and historical memory.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are NEEL, a highly sophisticated AI Life Coach and Productivity strategist.
            
            MEMORY CONTEXT:
            You will be provided with past summaries. Use them to identify trends. 
            If a problem is recurring, highlight it. If a user has improved compared to last month, congratulate them.

            PHILOSOPHY:
            - You relate everything back to the user's Primary Goal.
            - You speak with nuance.
            """),
            ("human", """
            Goal: {goal}
            Focus Areas: {focus}
            
            Current Analytics:
            - Activity Distribution: {distribution}
            - Recent Outcomes: {outcomes}

            Historical Context (Past Insights):
            {history}

            User Specific Question/Query:
            {query}

            Analyze current behavior vs goals, keeping historical trends in mind. Respond to the user's specific query if provided, otherwise provide a general progress assessment.
            """)
        ])

        chain = prompt | self.llm | StrOutputParser()
        
        history_text = "\n".join([f"- {s['date']}: {s['insight']}" for s in historical_summaries]) if historical_summaries else "No previous history found."

        return chain.invoke({
            "goal": user_profile.get("primary_goal"),
            "focus": user_profile.get("focus_areas"),
            "distribution": analytics.get("activity_distribution"),
            "outcomes": analytics.get("recent_outcomes"),
            "history": history_text,
            "query": user_profile.get("user_query", "No specific query provided.")
        })
