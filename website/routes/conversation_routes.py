"""
Module for handling conversation-related routes in the ChatFlow app.

Routes:
    - POST /create_private_chat:
        Creates a private chat between the current user and another user.
    - GET /chats/<chat_id>/history:
        Retrieves the chat history for a specific conversation
            and marks messages as read.
"""
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required

from website import db
from ..models.user import User
from ..models.conversation import Conversation
from ..models.message import Message
from ..models.group import Group


# Define conversation blueprint
conversation_routes_bp = Blueprint('conversation', __name__)


@conversation_routes_bp.route('/create_private_chat', methods=['POST'])
@login_required
def create_private_chat():
    """
    Route to create a private chat between the current user and another user.

    This endpoint allows the current user to create a private chat
        with another user, If a conversationa already exists,
            the existing chat's ID will be returned.

    Request:
        - JSON body containing 'chat_user_id':
            ID of the user to start a chat with.

    Response:
        - If the chat already exists:
            JSON response with a message and the existing chat ID.
        - If the chat is successfully created:
            JSON response with the new chat ID.
        - If an error occurs: JSON response with the error message.
    """
    try:
        # Get the ID of the user to chat with from the request JSON
        chat_user_id = request.json.get('chat_user_id')

        # Find the user by ID
        user = User.query.filter_by(id=chat_user_id).first()
        if not user:
            # If the user is not found, return a 404 error
            return jsonify({"error": "User not found"}), 404

        # Check if a conversation already exists between the current user
        # and the target user
        existing_chat = Conversation.query.filter(
            ((Conversation.user1_id == chat_user_id) &
             (Conversation.user2_id == current_user.id)) |
            ((Conversation.user2_id == chat_user_id) &
             (Conversation.user1_id == current_user.id))
        ).first()

        if existing_chat:
            # Empty response if the chat already exists
            return jsonify({})

        # Create a new conversation if no existing chat is found
        new_conversation = Conversation(
            user1_id=current_user.id,
            user2_id=chat_user_id,
            type='private_chat'
        )
        # Add the new conversation to the database session
        # and commit the changes
        db.session.add(new_conversation)
        db.session.commit()

        # Return the ID of the new chat
        return jsonify({"chat_id": new_conversation.id})
    except Exception as e:
        # Return a 500 error with the exception message
        return jsonify({"error": str(e)}), 500


@conversation_routes_bp.route('/chats/<chat_id>/history', methods=['GET'])
@login_required
def get_chat_history(chat_id):
    """
    Loads chat history for a specific conversation and marks messages as read.

    Args:
        chat_id (str): The ID of the conversation to retrieve the history for.

    Returns:
        JSON: A list of messages in the conversation
        If the conversation is not found, returns a 404 error with a message.
    """
    # Fetch the conversation based on the provided chat_id
    conversation = Conversation.query.filter_by(id=chat_id).first()

    # If the conversation is not found, return a 404 error
    if not conversation:
        return jsonify({"error": "Conversation not found"}), 404

    # Fetch all messages related to this conversation, ordered by timestamp
    messages = Message.query.filter_by(
        conversation_id=chat_id).order_by(Message.timestamp.asc()).all()

    # List to store message data to be returned
    message_data = []
    # List to store unread messages for marking them as read
    unread_messages = []

    for message in messages:
        # Add the message details to the response data
        message_data.append({
            'id': message.id,
            'sender_id': message.sender_id,
            'receiver_id': message.receiver_id,
            'sender': message.sender.name,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'is_read': message.is_read
        })

        # Mark unread messages as read if they are sent to the current user
        if not message.is_read and message.receiver_id == current_user.id:
            message.is_read = True
            unread_messages.append(message)

    # Commit the changes to mark unread messages as read
    if unread_messages:
        try:
            db.session.commit()
        except Exception as e:
            # Roll back the session
            db.session.rollback()

    # Return the chat history as JSON
    return jsonify({'messages': message_data})
