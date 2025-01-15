""" Moudle that contains the notification class. """
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from website import db
from uuid import uuid4


class Notification(db.Model):
    """
    Represents a notification for a user in the ChatFlow application.

    Attributes:
        id (str): Unique identifier for the notification (UUID).
        user_id (str): User ID to whom the notification belongs
            (foreign key to the User table).
        message (str): The content of the notification.
        is_read (bool):
            Indicates whether the notification has been read by the user.
        timestamp (datetime): The time the notification was created.
        type (str): The type of notification (e.g., "message", "alert").
        user (relationship):A relationship with the User class,
            linking the notification to the user.

    Methods:
        mark_as_read(): Marks the notification as read.
        __repr__(): Provides a string representation of the notification.
    """
    __tablename__ = 'notifications'
    id = Column(String(255), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(255), ForeignKey('users.id'), nullable=False)
    message = Column(String(255), nullable=False)
    is_read = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    type = Column(String(50), nullable=False)
    user = relationship('User', backref='notifications')

    def mark_as_read(self):
        """
        Marks the notification as read.

        This method updates the `is_read` field to True
            and commits the change to the database.
        """
        self.is_read = True
        db.session.commit()

    def __repr__(self):
        """
        Returns a string representation of the notification.

        Returns:
            str: A string representing the notification object.
        """
        return (f"<Notification(id='{self.id}', "
                f"user_id='{self.user_id}', "
                f"message='{self.message}')>")
