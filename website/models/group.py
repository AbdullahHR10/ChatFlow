""" Module that contains the Group class. """
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from website import db
from uuid import uuid4
from .conversation import Conversation


class Group(db.Model):
    """
    Represents a group chat in the ChatFlow application.

    Attributes:
        id (str): Unique identifier for the group, generated using UUID.
        group_name (str):
            Name of the group chat (e.g., "Developers' Hangout").
        group_description (str, optional): A brief description of the group.
        group_image (str, optional): URL or path to the group's image.
        created_at (datetime): Timestamp of when the group was created.
        updated_at (datetime):
            Timestamp of the last update to the group details.
        owner_id (str): ID of the user who owns the group.
        owner (User): Relationship to the User model,
            representing the group's owner.
        group_members (relationship):
            A dynamic relationship to GroupMembership,
                representing all members of the group.
    """

    __tablename__ = 'groups'
    id = Column(String(255), primary_key=True, default=lambda: str(uuid4()))
    group_name = Column(String(100), nullable=False)
    group_description = Column(Text, nullable=True)
    group_image = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    owner_id = Column(String(255), ForeignKey('users.id'), nullable=False)
    owner = relationship('User', backref='owned_groups')
    group_members = relationship(
        'GroupMembership', back_populates='group',
        lazy='dynamic', cascade='all, delete-orphan'
    )

    def add_member(self, user_id: str):
        """
        Adds a new member to the group.

        Args:
            user_id (str): The ID of the user to be added.

        Raises:
            IntegrityError: If the user is already a member of the group.
        """
        new_member = GroupMembership(id=self.id, user_id=user_id)
        db.session.add(new_member)
        db.session.commit()

    def remove_member(self, user_id: str):
        """
        Removes a member from the group.

        Args:
            user_id (str): The ID of the user to be removed.

        Raises:
            Exception: If the user is not found in the group.
        """
        membership = GroupMembership.query.filter_by(id=self.id,
                                                     user_id=user_id).first()
        if membership:
            db.session.delete(membership)
            db.session.commit()

    def create_group_conversation(self):
        """
        Creates a conversation associated with this group.

        Returns:
            Conversation: The newly created group conversation object.
        """
        conversation = Conversation(
            id=self.id,
            type='group',
            user1_id=self.owner_id,  # Initial user (group owner)
            user2_id=None  # Not applicable for groups
        )
        db.session.add(conversation)
        db.session.commit()
        return conversation

    def __repr__(self):
        """
        Returns a string representation of the Group object.
        """
        return (
            f"<Group(id='{self.id}', group_name='{self.group_name}', "
            f"owner_id='{self.owner_id}')>"
        )


class GroupMembership(db.Model):
    """
    Represents a user's membership in a group.

    Attributes:
        id (str): The ID of the group the user belongs to.
        user_id (str): The ID of the user who is a member of the group.
        joined_at (datetime): Timestamp of when the user joined the group.
        role (str):
            The role of the user in the group (e.g., 'admin', 'member').
        group (Group):
            Relationship to the Group model, representing the group.
        user (User): Relationship to the User model, representing the member.
    """

    __tablename__ = 'group_memberships'
    id = Column(String(255), ForeignKey('groups.id'), primary_key=True)
    user_id = Column(String(255), ForeignKey('users.id'), primary_key=True)
    joined_at = Column(DateTime, default=datetime.utcnow)
    role = Column(String(20), default='member')
    group = relationship('Group', backref='memberships')
    user = relationship('User', backref='group_memberships')

    def __repr__(self):
        """
        Returns a string representation of the GroupMembership object.
        """
        return (
            f"<GroupMembership(id='{self.id}', "
            f"user_id='{self.user_id}')>"
        )
