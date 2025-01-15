""" Module that contains the User class. """
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Text, Boolean, Date
from flask_login import UserMixin
from website import db
from .friendship import Friendship
from werkzeug.utils import secure_filename
from website.config import Config
import os
import random


class User(db.Model, UserMixin):
    """
    Represents a user in the ChatFlow application.

    Attributes:
        id (str): Unique identifier for the user (UUID).
        username (str): Username of the user.
        phone_number (str): Phone number of the user (must be unique).
        phone_number_is_private (bool):
            Indicates if the phone number is private.
        password (str): User's hashed password.
        profile_picture (str): Path to the user's profile picture.
        status (str): Current online status (e.g., "offline").
        custom_status (str): Custom status set by the user.
        last_seen (datetime): Timestamp of the user's last activity.
        last_seen_is_private (bool):
            Indicates if the last seen time is private.
        created_at (datetime): Account creation timestamp.
        updated_at (datetime): Last account update timestamp.
        bio (str): User's biography.
        bio_is_private (bool): Indicates if the bio is private.
        birthdate (datetime): User's birthdate.
        birthdate_is_private (bool): Indicates if the birthdate is private.
        location (str): User's location.
        location_is_private (bool): Indicates if the location is private.
        facebook_link (str): Link to the user's Facebook profile.
        discord_id (str): User's Discord ID.
        github_link (str): Link to the user's GitHub profile.
        youtube_link (str): Link to the user's YouTube channel.
        website_link (str): User's personal website link.
        allow_friend_requests (bool):
            Indicates if the user accepts friend requests.
        role (str): User's role (e.g., "user", "admin").
        last_login (datetime): Timestamp of the user's last login.
        job_title (str): User's job title.
        job_title_is_private (bool): Indicates if the job title is private.
        friend_id (str): Unique identifier for friends.

    Methods:
        change_username(new_username): Changes the user's username.
        change_password(new_password): Changes the user's password.
        change_profile_picture(new_profile_picture):
            Changes the user's profile picture.
        change_bio(new_bio): Changes the user's bio.
        update_last_login(): Updates the user's last login timestamp.
        save_profile_picture(file):
            Saves the uploaded profile picture and updates the user record.
        connect_friends(): Returns a list of connected friends for the user.
        check_friendship_status(friend_id):
            Returns the friendship status with a particular friend.
        allowed_file(filename):
            Checks if the file has a valid extension for uploading.
    """
    __tablename__ = 'users'
    id = Column(String(255), primary_key=True, default=lambda: str(uuid4()),
                nullable=False)
    name = Column(String(50), nullable=False)
    phone_number = Column(String(15), unique=True, nullable=False)
    phone_number_is_private = Column(Boolean, nullable=False, default=False)
    password = Column(String(255), nullable=False)
    profile_picture = Column(String(255), nullable=True)
    status = Column(String(20), default="offline")
    custom_status = Column(String(20), nullable=True)
    last_seen = Column(DateTime, nullable=True)
    last_seen_is_private = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    bio = Column(Text, nullable=True)
    bio_is_private = Column(Boolean, nullable=False, default=False)
    birthdate = Column(Date, nullable=True)
    birthdate_is_private = Column(Boolean, nullable=False, default=False)
    location = Column(String(255), nullable=True)
    location_is_private = Column(Boolean, nullable=False, default=False)
    facebook_link = db.Column(db.String(255), nullable=True)
    discord_id = db.Column(db.String(255), nullable=True)
    github_link = db.Column(db.String(255), nullable=True)
    youtube_link = db.Column(db.String(255), nullable=True)
    website_link = db.Column(db.String(255), nullable=True)
    allow_friend_requests = Column(Boolean, nullable=False, default=True)
    role = Column(String(20), default="user")
    last_login = Column(DateTime, nullable=True)
    job_title = Column(String(255), nullable=True)
    job_title_is_private = Column(Boolean, nullable=False, default=False)
    friend_id = Column(String(10),
                       unique=True,
                       nullable=False,
                       default=lambda:
                       str(random.randint(10000000, 99999999)))
    conversations_user1 = db.relationship('Conversation',
                                          foreign_keys='Conversation.user1_id',
                                          backref='user1_conversation',
                                          lazy=True)
    conversations_user2 = db.relationship('Conversation',
                                          foreign_keys='Conversation.user2_id',
                                          backref='user2_conversation',
                                          lazy=True)

    def change_username(self, new_username: str):
        """
        Changes the user's username.

        Args:
            new_username (str): The new username to set.
        """
        self.username = new_username
        db.session.commit()

    def change_password(self, new_password: str):
        """
        Changes the user's password.

        Args:
            new_password (str): The new password to set.
        """
        self.password = new_password
        db.session.commit()

    def change_profile_picture(self, new_profile_picture: str):
        """
        Changes the user's profile picture.

        Args:
            new_profile_picture (str): The new profile picture file path.
        """
        self.profile_picture = new_profile_picture
        db.session.commit()

    def change_bio(self, new_bio: str):
        """
        Changes the user's bio.

        Args:
            new_bio (str): The new bio to set.
        """
        self.bio = new_bio
        db.session.commit()

    def update_last_login(self):
        """
        Updates the user's last login timestamp to the current time.
        """
        self.last_login = datetime.utcnow()
        db.session.commit()

    def save_profile_picture(self, file):
        """
        Saves the uploaded profile picture and updates the user record.

        Args:
            file (FileStorage): The uploaded file object.
        """
        if file and self.allowed_file(file.filename):
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(
                f"{self.id}_profile_picture.{file_extension}")
            file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
            self.profile_picture = filename
            db.session.commit()

    def connect_friends(self):
        """
        Returns a list of connected friends for the user.

        Returns:
            list: A list of dictionaries with friend information such as ID,
                username, profile picture, and friendship status.
        """
        friends = Friendship.get_friends(self.id)
        connected_friends = []

        for friend_id in friends:
            friend = User.query.get(friend_id)
            connected_friends.append({
                'friend_id': friend.id,
                'username': friend.username,
                'profile_picture': friend.profile_picture,
                'status': self.check_friendship_status(friend_id)
            })

        return connected_friends

    def check_friendship_status(self, friend_id):
        """
        Checks the friendship status with a specific friend.

        Args:
            friend_id (str): The ID of the friend.

        Returns:
            str: The friendship status
                (e.g., 'pending', 'accepted', 'rejected')
                or None if no friendship exists.
        """
        friendship = db.session.query(Friendship).filter(
            ((Friendship.user_id_1 == self.id) &
             (Friendship.user_id_2 == friend_id)) |
            ((Friendship.user_id_1 == friend_id) &
             (Friendship.user_id_2 == self.id))
        ).first()
        return friendship.status if friendship else None

    @staticmethod
    def allowed_file(filename):
        """
        Checks if the file has a valid extension.

        Args:
            filename (str): The name of the file.

        Returns:
            bool: True if the file has a valid extension, False otherwise.
        """
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

    def __repr__(self):
        """
        Returns a string representation of the user.

        Returns:
            str: String representation of the user object.
        """
        return (f"<User(id='{self.id}', username='{self.username}', "
                f"phone_number='{self.phone_number}', bio='{self.bio}')>")
