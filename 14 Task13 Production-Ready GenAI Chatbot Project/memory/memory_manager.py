from database.db import SessionLocal
from database.models import ChatHistory

def save_message(user_id, role, message):
    db = SessionLocal()
    chat = ChatHistory(user_id=user_id, role=role, message=message)
    db.add(chat)
    db.commit()
    db.close()

def get_chat_history(user_id):
    db = SessionLocal()
    chats = db.query(ChatHistory).filter(ChatHistory.user_id == user_id).all()
    db.close()
    return chats
