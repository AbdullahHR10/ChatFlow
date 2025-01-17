""" Module that contains the Message class. """
from datetime import datetime
from sqlalchemy import (
    Column, String, ForeignKey, Text, DateTime, Boolean, JSON
)
from sqlalchemy.orm import relationship
from uuid import uuid4
from website import db


class Message(db.Model):
    """
    Represents a message between users in the ChatFlow application.

    Attributes:
        id (str): Unique identifier for the message.
        conversation_id (str):
            Identifier for the conversation the message belongs to.
        content (str): Content of the message.
        timestamp (datetime): Timestamp when the message was created.
        group_id (str, optional):
            Identifier for the group the message was sent to (if any).
        is_read (bool): Whether the message has been read.
        sender_id (str): Identifier for the user who sent the message.
        receiver_id (str, optional):
            Identifier for the user who received the message.
        media_type (str, optional):
            Type of media attached to the message (e.g., 'image', 'video').
        media_url (str, optional): URL of the media attached to the message.

    Methods:
        mark_as_read():
            Marks the message as read by updating the `is_read` attribute.
            Commits the change to the database.
        delete_message():
            Permanently deletes the message from the database.
            Commits the deletion to the database.
        __repr__():
            Returns a string representation of the Message object.
    """

    __tablename__ = 'messages'
    id = Column(String(255), primary_key=True, default=lambda: str(uuid4()))
    conversation_id = Column(String(255),
                             ForeignKey('conversations.id'), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    group_id = Column(String(255),
                      ForeignKey('groups.id'), nullable=True)
    is_read = Column(Boolean, default=False)
    conversation = relationship('Conversation',
                                backref='conversation_messages')
    sender_id = Column(String(255), ForeignKey('users.id'), nullable=False)
    sender = relationship('User', backref='sent_messages',
                          primaryjoin="Message.sender_id == User.id")
    receiver_id = db.Column(String(255), db.ForeignKey('users.id'))
    receiver = db.relationship('User', foreign_keys=[receiver_id],
                               backref='received_messages')
    media_type = Column(String(50), nullable=True)
    media_url = Column(String(255), nullable=True)

    def mark_as_read(self):
        """
        Marks the message as read by updating the `is_read` attribute.

        Commits the change to the database.
        """
        self.is_read = True
        db.session.commit()

    def delete_message(self):
        """
        Permanently deletes the message from the database.

        Commits the deletion to the database.
        """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """
        Returns a string representation of the Message object.

        Returns:
            str: A string representing the Message object with key attributes.
        """
        return (f"<Message(id='{self.id}', sender_id='{self.sender_id}', "
                f"receiver_id='{self.receiver_id}', "
                f"timestamp='{self.timestamp}', "
                f"is_read={self.is_read})>")
