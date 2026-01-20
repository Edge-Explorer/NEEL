from sqlalchemy.orm import Session
from backend.models import ChatMessage
from typing import List

class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_message(self, user_id: int, role: str, content: str) -> ChatMessage:
        message = ChatMessage(
            user_id=user_id,
            role=role,
            content=content
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_history(self, user_id: int, limit: int = 50) -> List[ChatMessage]:
        return self.db.query(ChatMessage).filter(
            ChatMessage.user_id == user_id
        ).order_by(ChatMessage.timestamp.asc()).limit(limit).all()

    def get_recent_context(self, user_id: int, limit: int = 5) -> List[ChatMessage]:
        """Returns the most recent messages for AI context."""
        return self.db.query(ChatMessage).filter(
            ChatMessage.user_id == user_id
        ).order_by(ChatMessage.timestamp.desc()).limit(limit).all()
