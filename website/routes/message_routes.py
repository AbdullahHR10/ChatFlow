"""
Module that contains message routes in the ChatFlow application.

Routes:
    - DELETE /messages/<message_id>/delete:
        Deletes a message if the current user is the sender,
            and emits a real-time update to all users in the conversation.
"""

from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from website import db
from ..models.message import Message
from website import socketio

message_routes_bp = Blueprint('message', __name__)


@message_routes_bp.route('/messages/<message_id>/delete', methods=['DELETE'])
@login_required
def delete_message(message_id):
    """
    Deletes a message by its ID.

    - Retrieves the message by its ID.
    - Checks if the message exists.
    - Verifies that the current user is the sender of the message.
    - Deletes the message if the user is authorized.
    - Emits a chat history update event to all users in the conversation.
    - Returns a success message or error message in the response.

    Args:
        message_id (str): The ID of the message to be deleted.

    Returns:
        JSON response with success or error status.
    """
    try:
        # Retrieve the message from the database
        message = Message.query.filter_by(id=message_id).first()

        # If the message does not exist, return a 404 error
        if not message:
            return jsonify({"error": "Message not found"}), 404

        # Ensure the current user is the sender of the message
        if message.sender_id != current_user.id:
            return jsonify({
                "error": "You are not authorized to delete this message"}), 403

        # Get the conversation ID before deleting the message
        conversation_id = message.conversation_id

        # Delete the message from the database
        db.session.delete(message)
        db.session.commit()

        # Emit an event to update the chat history in real-time
        # for the conversation
        socketio.emit(
            'chat_history_update',
            {'conversation_id': conversation_id},
            room=f"conversation_{conversation_id}",
        )

        # Return a success response after deletion
        return jsonify({"success": True,
                        "message": "Message deleted successfully"})

    except Exception as e:

        print(f"Error deleting message: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
