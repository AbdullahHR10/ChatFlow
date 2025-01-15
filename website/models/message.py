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
        reactions (dict):
            Dictionary of reactions to the message,
                where key is user_id and value is the emoji.
        sender_id (str): Identifier for the user who sent the message.
        receiver_id (str, optional):
            Identifier for the user who received the message.
        media_type (str, optional):
            Type of media attached to the message (e.g., 'image', 'video').
        media_url (str, optional): URL of the media attached to the message.
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
    reactions = Column(JSON, default={})
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

    def reply_to_message(self, reply_content: str):
        """
        Creates a new message that replies to this message.

        Args:
            reply_content (str): The content of the reply message.

        Returns:
            Message: The newly created reply message.
        """
        reply_message = Message(
            sender_id=self.receiver_id,
            receiver_id=self.sender_id,
            content=reply_content,
            timestamp=datetime.utcnow()
        )
        db.session.add(reply_message)
        db.session.commit()
        return reply_message

    def add_reaction(self, user_id: str, emoji: str):
        """
        Adds a reaction (emoji) to the message.

        If the user has already reacted, it updates their reaction.

        Args:
            user_id (str): The ID of the user reacting to the message.
            emoji (str): The emoji representing the reaction.
        """
        self.reactions[user_id] = emoji
        db.session.commit()

    def remove_reaction(self, user_id: str):
        """
        Removes a user's reaction from the message.

        Args:
            user_id (str): The ID of the user whose reaction is to be removed.
        """
        if user_id in self.reactions:
            del self.reactions[user_id]
            db.session.commit()

    def get_reactions(self):
        """
        Returns all reactions to the message as a dictionary.

        Returns:
            dict: A dictionary of reactions,
                with user_id as the key and emoji as the value.
        """
        return self.reactions

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
