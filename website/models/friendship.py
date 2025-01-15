""" Moudle that contains the Friendship class. """
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.schema import UniqueConstraint
from datetime import datetime
from website import db
from enum import Enum
from uuid import uuid4


class FriendshipStatus(Enum):
    """
    Enum to represent the different friendship statuses.

    Attributes:
        PENDING (str): Represents a pending friend request.
        ACCEPTED (str): Represents an accepted friendship.
        DECLINED (str): Represents a declined friend request.
        BLOCKED (str): Represents a blocked user.
    """
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    BLOCKED = "blocked"


class Friendship(db.Model):
    """
    Represents a friendship between two users in the ChatFlow application.

    Attributes:
        id (str): Unique identifier for the friendship.
        user_id_1 (str): ID of the first user in the friendship.
        user_id_2 (str): ID of the second user in the friendship.
        created_at (datetime): Timestamp of when the friendship was created.
        status (str):Current status of the friendship
            (e.g., "pending", "accepted", "declined", "blocked").
        user_1 (User): Relationship to the first user in the friendship.
        user_2 (User): Relationship to the second user in the friendship.

    Methods:
        accept_request: Accepts a pending friend request.
        decline_request: Declines a pending friend request.
        remove_friendship: Removes an existing friendship.
        block_user: Blocks a user.
        unblock_user: Unblocks a user.
        get_pending_requests:
            Retrieves a list of incoming pending friend requests for a user.
        get_outgoing_requests:
            Retrieves a list of
                outgoing pending friend requests from the user.
        get_friends: Retrieves a list of friends for a user.
        get_user_by_friend_id: Retrieves a user by their friend ID.
    """

    __tablename__ = 'friendships'
    id = Column(String(255), primary_key=True, default=lambda: str(uuid4()))
    user_id_1 = Column(String(255), ForeignKey('users.id'), nullable=False)
    user_id_2 = Column(String(255), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default=FriendshipStatus.PENDING.value)
    user_1 = relationship('User',
                          foreign_keys=[user_id_1], backref='friendships_1')
    user_2 = relationship('User',
                          foreign_keys=[user_id_2], backref='friendships_2')
    __table_args__ = (
        UniqueConstraint('user_id_1', 'user_id_2', name='unique_friendship'),
    )

    def accept_request(self):
        """
        Accepts a pending friend request.

        Changes the friendship status to 'accepted'
            and commits the changes to the database.
        """
        if self.status == FriendshipStatus.PENDING.value:
            self.status = FriendshipStatus.ACCEPTED.value
            db.session.commit()

    def decline_request(self):
        """
        Declines a pending friend request.

        Deletes the friendship entry from the database
            and commits the changes.
        """
        if self.status == FriendshipStatus.PENDING.value:
            db.session.delete(self)
            db.session.commit()

    def remove_friendship(self):
        """
        Removes an existing friendship.

        Deletes the friendship entry from the database
            and commits the changes.
        """
        if self.status == FriendshipStatus.ACCEPTED.value:
            db.session.delete(self)
            db.session.commit()

    def block_user(self):
        """
        Blocks a user.

        Changes the friendship status to 'blocked'
            and commits the changes to the database.
        """
        self.status = FriendshipStatus.BLOCKED.value
        db.session.commit()

    def unblock_user(self):
        """
        Unblocks a user.

        Changes the friendship status back to 'pending'
            and commits the changes to the database.
        """
        if self.status == FriendshipStatus.BLOCKED.value:
            self.status = FriendshipStatus.PENDING.value
            db.session.commit()

    @staticmethod
    def get_pending_requests(user_id):
        """
        Retrieves a list of incoming pending friend requests for a user.

        Args:
            user_id (str): The ID of the user for whom
                the pending requests are retrieved.

        Returns:
            list:A list of Friendship objects
                representing pending friend requests.
        """
        return db.session.query(Friendship).filter(
            (Friendship.user_id_2 == user_id) &
            (Friendship.status == FriendshipStatus.PENDING.value)
        ).all()

    @staticmethod
    def get_outgoing_requests(user_id):
        """
        Retrieves a list of outgoing pending friend requests from the user.

        Args:
            user_id (str): The ID of the user for whom
                the outgoing requests are retrieved.

        Returns:
            list: A list of Friendship objects
                representing outgoing pending friend requests.
        """
        return db.session.query(Friendship).filter(
            (Friendship.user_id_1 == user_id) &
            (Friendship.status == FriendshipStatus.PENDING.value)
        ).all()

    @staticmethod
    def get_friends(user_id):
        """
        Retrieves a list of friends for a user.

        Args:
            user_id (str): The ID of the user whose friends are retrieved.

        Returns:
            list: A list of user IDs representing the user's friends.
        """
        friendships = db.session.query(Friendship).filter(
            ((Friendship.user_id_1 == user_id) |
             (Friendship.user_id_2 == user_id)) &
            (Friendship.status == FriendshipStatus.ACCEPTED.value)
        ).all()
        return [f.user_id_1 if f.user_id_2 == user_id
                else f.user_id_2 for f in friendships]

    @staticmethod
    def get_user_by_friend_id(friend_id):
        """
        Retrieves a user by their friend ID.

        Args:
            friend_id (str): The friend ID of the user.

        Returns:
            User: The user object associated with the given friend ID.
        """
        return db.session.query('User').filter_by(friend_id=friend_id).first()

    def __repr__(self):
        """
        Returns a string representation of the Friendship object.

        Returns:
            str: A string representing the Friendship object.
        """
        return (f"<Friendship(user_id_1='{self.user_id_1}', "
                f"user_id_2='{self.user_id_2}', status='{self.status}')>")
