import json
from datetime import datetime
from extensions import db

class Conversation(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="conversation ID")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, comment="user ID")
    user = db.relationship("User", backref="conversations", lazy=True)
    title = db.Column(db.String(255), default="New conversation", comment="title")
    created_at = db.Column(db.DateTime, default=datetime.now, comment="created time")
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment="updated time")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "message_count": len(self.messages) if hasattr(self, "messages") else 0,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }

class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="message ID")
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversations.id"), nullable=False, comment="conversation ID")
    conversation = db.relationship("Conversation", backref=db.backref("messages", lazy="dynamic", order_by="Message.created_at"), lazy=True)
    role = db.Column(db.Enum("user", "assistant"), nullable=False, comment="role")
    content = db.Column(db.Text, nullable=False, comment="content")
    sources = db.Column(db.Text, comment="sources (JSON)")
    created_at = db.Column(db.DateTime, default=datetime.now, comment="created time")

    def to_dict(self):
        try:
            parsed_sources = json.loads(self.sources) if self.sources else []
        except (json.JSONDecodeError, TypeError):
            parsed_sources = self.sources or []
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "role": self.role,
            "content": self.content,
            "sources": parsed_sources,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }