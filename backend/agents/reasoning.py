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

    def generate_guidance(self, user_profile: Dict[str, Any], analytics: Dict[str, Any], historical_summaries: List[Dict[str, Any]] = None, chat_context: List[Dict[str, Any]] = None) -> str:
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
            - You speak with nuance and a friendly, conversational tone.
            - IMPORTANT: Do NOT use Markdown formatting like bold (**text**), italics (*text*), or markdown headers. Use plain text and emojis only to keep the chat clean.
            - Use single newlines for spacing.

            AUTO-LOGGING FEATURE:
            - If the user explicitly mentions they completed a task or worked for some time (e.g., "I debugged for 2 hours", "Just finished a 30m workout"), you MUST detect it.
            - At the VERY END of your response, add this exact tag: [AUTO_LOG: activity_name, duration_int, short_description]
            - Use activity names from: Coding, Research, Learning, Meeting, Exercise, Meditation, Reading, Leisure.
            - If duration is not mentioned, estimate it or use 30.

            GOAL & PROFILE UPDATES:
            - If the user says something like "My new goal is [Goal]" or "I want to focus on [A, B, C]", use this tag at the VERY END: [UPDATE_PROFILE: new_primary_goal, focus_areas_comma_separated]
            - Only include the field they changed. Leave others empty if not mentioned.
            """),
            ("human", """
            Recent Chat Context:
            {chat_history}

            Goal: {goal}
            Focus Areas: {focus}
            
            Current Analytics:
            - Activity Distribution: {distribution}
            - Recent Outcomes: {outcomes}

            Historical Context (Past Insights):
            {history}

            User Specific Question/Query:
            {query}

            Analyze current behavior vs goals, keeping historical trends and recent conversation context in mind. Respond to the user's specific query if provided, otherwise provide a general progress assessment.
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
            "query": user_profile.get("user_query", "No specific query provided."),
            "chat_history": "\n".join([f"{m['role'].upper()}: {m['content']}" for m in chat_context]) if chat_context else "No recent chat history."
        })

    def generate_onboarding_guidance(self, check_reason: str, query: str, analytics: Dict[str, Any], history: List[Dict[str, Any]] = None, chat_context: List[Dict[str, Any]] = None) -> str:
        """
        Generates a personalized, context-aware onboarding message that acknowledges 
        recent progress while explaining why more data is still needed.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are NEEL, a sophisticated AI Life Coach. 
            The user is currently in the 'Onboarding/Data Gathering' phase (first 7 days).
            
            YOUR TASK:
            1. Acknowledge what they've done recently using the 'Current Analytics' below.
            2. If they have activities logged, mention one specifically (e.g., "I see you spent time on [Activity] yesterday").
            3. Explain that while you're seeing their progress, you still need a bit more data (total 120+ mins) to unlock full strategic powers.
            4. Keep it warm, professional, and conversational.

            AUTO-LOGGING FEATURE:
            - If the user reports new work in this chat, add [AUTO_LOG: activity_name, duration_int, short_description] at the very end.
            
            FORMATTING RULES:
            - NO markdown symbols like ** or *.
            - NO bullet points with dashes.
            - Use emojis.
            - Use plain text and friendly paragraphs.
            """),
            ("human", """
            Recent Chat Context:
            {chat_history}

            Reason for data gap: {reason}
            User's specific question: {query}
            
            Current Analytics: {analytics}
            Historical Context: {history}
            
            Please provide a conversational response that builds trust by showing you are tracking their specific journey and remembering recent messages.
            """)
        ])

        history_text = "\n".join([f"- {s['date']}: {s['insight']}" for s in history]) if history else "No previous history."
        chain = prompt | self.llm | StrOutputParser()
        
        return chain.invoke({
            "reason": check_reason, 
            "query": query,
            "analytics": analytics,
            "history": history_text,
            "chat_history": "\n".join([f"{m['role'].upper()}: {m['content']}" for m in chat_context]) if chat_context else "No recent chat history."
        })
