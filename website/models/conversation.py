""" Module that contaisn the Conversation class. """
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4
from .message import Message
from website import db


class Conversation(db.Model):
    """
    Represents a conversation between users or in a group chat.

    Attributes:
        id (str): Unique identifier for the conversation.
        type (str): Type of conversation, such as 'individual' or 'group'.
        user1_id (str, optional):
            ID of the first user in the conversation (if applicable).
        user2_id (str, optional):
            ID of the second user in the conversation (if applicable).
        group_id (str, optional):
            ID of the group the conversation belongs to (if applicable).
        created_at (datetime): Timestamp when the conversation was created.
        updated_at (datetime):
            Timestamp when the conversation was last updated.
        last_message (str, optional):
            The content of the last message in the conversation.
        last_message_date (datetime, optional):
            Timestamp of when the last message was sent.
        user1 (User): Relationship to the first user in the conversation.
        user2 (User): Relationship to the second user in the conversation.
        group (Group): Relationship to the group associated
            with the conversation (if applicable).
        messages (list):
            List of Message objects associated with the conversation.

    Methods:
        __repr__: Returns a string representation of the Conversation object.
    """

    __tablename__ = 'conversations'
    id = Column(String(255), primary_key=True, default=lambda: str(uuid4()))
    type = Column(String(20), nullable=False)
    user1_id = Column(String(255), ForeignKey('users.id'), nullable=True)
    user2_id = Column(String(255), ForeignKey('users.id'), nullable=True)
    group_id = Column(String(255), ForeignKey('groups.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime,
                        default=datetime.utcnow, onupdate=datetime.utcnow)
    last_message = db.Column(String(1024), nullable=True)
    last_message_date = db.Column(DateTime, nullable=True)
    user1 = relationship('User', foreign_keys=[user1_id])
    user2 = relationship('User', foreign_keys=[user2_id])
    group = relationship('Group', backref='conversations')
    messages = relationship('Message', backref='conversation_messages')

    def __repr__(self):
        """
        Returns a string representation of the Conversation object.

        Returns:
            str: A string representing the Conversation object,
                including its ID and type.
        """
        return f"<Conversation(id='{self.id}', type='{self.type}')>"
