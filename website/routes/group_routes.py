"""
Module that contains group routes in the ChatFlow application.

Routes:
    - POST /group/create:
        Handles the creation of a new group.
    - POST /group/delete/<id>:
        Deletes a group by its ID.
    - GET /groups/<group_id>/history:
        Retrieves and displays the chat history for a specific group.
    - POST /group/<group_id>/add_member:
        Adds members to a specified group.
    - POST /group/<group_id>/leave:
        Allows a user to leave a group.
    - POST /group/<group_id>/kick_member:
        Kicks a member from a specified group.
"""

from flask import Blueprint, request, jsonify, current_app, url_for, redirect
from flask_login import current_user, login_required

from website import db
from website.utils.allowed_file import allowed_file
from ..models.user import User
from ..models.conversation import Conversation
from ..models.message import Message
from ..models.group import Group, GroupMembership

import os
from datetime import datetime


# Define conversation blueprint
group_routes_bp = Blueprint('group', __name__)


@group_routes_bp.route('/group/create', methods=['POST'])
@login_required
def create_group():
    """
    Route to handle the creation of a new group.

    Returns:
        - On success: Redirects the user to the dashboard.
        - On failure: Returns a JSON response with an
            error message and HTTP status code 400 or 500.
    """
    try:
        # Extract the group name from the form data.
        group_name = request.form.get('group_name')

        # Extract the optional group description from the form data.
        group_description = request.form.get('group_description')

        # Extract the optional group image from the form data.
        group_image = request.files.get('group_image')

        # Ensure that a group name has been provided (it's a required field).
        if not group_name:
            return jsonify({"error": "Group name is required"}), 400

        # Create a new group instance in the database.
        # The group image is initially set to an empty string
        # and will be updated later.
        new_group = Group(
            group_name=group_name,
            group_description=group_description,
            group_image='',
            owner_id=current_user.id
        )

        # Add the group to the database session for saving.
        db.session.add(new_group)

        # Commit the changes to generate a group ID
        # (needed for the image file name).
        db.session.commit()

        # Handle the group image upload if provided.
        if group_image and allowed_file(group_image.filename):
            # Generate a secure filename using the group's ID
            # and the file's original extension.
            filename = f"{new_group.id}"
            f"{os.path.splitext(group_image.filename)[1]}"

            # Define the full file path where the image will be stored.
            file_path = os.path.join(
                current_app.config['GROUP_PICS_UPLOAD_FOLDER'], filename)

            # Save the uploaded image file to the specified path.
            group_image.save(file_path)

            # Update the group's image to reference the saved filename.
            new_group.group_image = filename
        else:
            # If no valid image was provided, assign a default group image.
            new_group.group_image = 'default_group.png'

        # Commit the changes to save the group image in the database.
        db.session.commit()

        # Add the current user as a member of the group with the "owner" role.
        owner_membership = GroupMembership(
            user_id=current_user.id,
            group=new_group,
            role="owner"
        )

        # Add the membership to the database session for saving.
        db.session.add(owner_membership)
        db.session.commit()

        # Create a conversation for the newly created group.
        new_conversation = Conversation(
            type='group',
            group_id=str(new_group.id),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # Add the conversation to the database session for saving.
        db.session.add(new_conversation)

        # Commit the changes to save the group conversation.
        db.session.commit()

        # Redirect the user to the dashboard
        # after successfully creating the group.
        return redirect(url_for('main_routes_bp.dashboard'))

    except Exception as e:
        # If an error occurs during the process,
        # return a JSON response with the error message.
        return jsonify({"error": str(e)}), 500


@group_routes_bp.route('/group/delete/<string:id>', methods=['POST'])
@login_required
def delete_group(id):
    """
    Route to delete a group by its ID.

    Args:
        id (str): The ID of the group to be deleted.

    Returns:
        Response:
        - On success: Redirects the user to the dashboard.
        - On failure: Returns a JSON response with an error message
            and corresponding HTTP status code.
    """
    try:
        # Query the group from the database by its ID.
        group = Group.query.filter_by(id=id).first()

        # If the group does not exist
        if not group:
            # return a 404 error indicating the group is not found.
            return jsonify({"error": "Group not found"}), 404

        # Ensure that the user making the request is the owner of the group.
        if group.owner_id != current_user.id:
            return jsonify({"error": "Unauthorized action"}), 403

        # Delete all messages associated with the group from the database.
        Message.query.filter_by(group_id=id).delete()

        # Proceed to delete the group from the database.
        db.session.delete(group)

        # Commit the transaction to apply all the changes.
        db.session.commit()

        # After successful deletion, redirect the user back to the dashboard.
        return redirect(url_for('main_routes_bp.dashboard'))

    except Exception as e:
        # If any exception occurs during the process,
        # catch it and return an error message.
        return jsonify({"error": str(e)}), 500


@group_routes_bp.route('/groups/<group_id>/history', methods=['GET'])
@login_required
def get_group_chat_history(group_id):
    """
    Route to retrieve and display the chat history for a specific group.

    Args:
        group_id (str):
            The ID of the group for which the chat history is being requested.

    Returns:
        Response:
        - On success: A JSON response with the chat history
        - On failure: A JSON response with an error message
            if the group is not found
    """
    # Fetch the group from the database using the provided group_id.
    group = Group.query.filter_by(id=group_id).first()

    # If the group does not exist
    if not group:
        # Return a 404 error indicating the group was not found.
        return jsonify({"error": "Group not found"}), 404

    # Fetch all messages associated with the group,
    # ordered by timestamp (ascending).
    messages = Message.query.filter_by(group_id=group_id).order_by(
                                                Message.timestamp.asc()).all()

    # Prepare lists to hold formatted message data and track unread messages.
    message_data = []
    unread_messages = []

    # Loop through each message to build the response data.
    for message in messages:
        # Get the sender's user object using the sender_id from the message.
        sender = User.query.get(message.sender_id)

        # If the sender exists, get their name; otherwise,
        # mark the sender as "Unknown".
        sender_name = sender.name if sender else 'Unknown'

        # Append the message data to the message_data list.
        message_data.append({
            'id': message.id,
            'sender_id': message.sender_id,
            'sender_name': sender_name,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'is_read': message.is_read
        })

        # If the message is unread and it is sent to the current user,
        # mark it as read.
        if not message.is_read and message.receiver_id == current_user.id:
            message.is_read = True
            unread_messages.append(message)

    # If there are any unread messages,
    # commit the changes to mark them as read in the database.
    if unread_messages:
        try:
            # Attempt to commit the changes to the database.
            db.session.commit()
        except Exception as e:
            # If an error occurs, print the error and roll back the changes.
            print(f"Error marking messages as read: {e}")
            db.session.rollback()

    # Return a JSON response with the message data,
    # representing the group chat history.
    return jsonify({'messages': message_data})


@group_routes_bp.route('/group/<string:group_id>/add_member', methods=['POST'])
@login_required
def add_member_to_group(group_id):
    """
    Route to add members to a specified group.

    Args:
        group_id (str): The ID of the group to add the members to.

    Returns:
        Response:
        - On success: A JSON response indicating the users were added.
        - On failure: A JSON response with an error message
    """
    try:
        # Extract member IDs from the request body
        members = request.json.get('members')
        if not members:
            # If no member IDs are provided, return an error
            return jsonify({"error": "User IDs are required"}), 400

        # Fetch the group from the database using the provided group_id
        group = Group.query.filter_by(id=group_id).first()
        if not group:
            # If the group is not found, return a 404 error with a message
            return jsonify(
                {"error": f"Group with ID {group_id} not found"}), 404

        # Check if the current user is the owner of the group
        if group.owner_id != current_user.id:
            # Return a 403 error indicating unauthorized action
            return jsonify({"error": "Unauthorized action"}), 403

        # Loop through the list of user IDs
        for user_id in members:
            # Fetch the user from the database
            user = User.query.filter_by(id=user_id).first()
            # If the user is not found,
            if not user:
                # Return a 404 error for the specific user
                return jsonify({"error": f"User {user_id} not found"}), 404

            # Check if the user is already a member of the group
            existing_membership = GroupMembership.query.filter_by(
                group=group, user_id=user_id).first()
            if existing_membership:
                # If the user is already a member, skip adding them
                continue

            # Create a new GroupMembership entry
            new_membership = GroupMembership(group=group, user_id=user_id)
            db.session.add(new_membership)

        # Commit the changes to the database
        db.session.commit()

        # Return a success message after successfully adding the users
        return jsonify(
            {"message": "Users added to the group successfully"}), 200

    except Exception as e:
        # Handle any unexpected errors by
        # returning a 500 error with the exception message
        return jsonify({"error": str(e)}), 500


@group_routes_bp.route('/group/<string:group_id>/leave', methods=['POST'])
@login_required
def leave_group(group_id):
    """
    Route to allow a user to leave a group.

    Args:
        group_id (str): The ID of the group to leave.

    Returns:
        JSON response indicating success or failure.
    """
    try:
        # Check if the group exists
        group = Group.query.filter_by(id=group_id).first()
        if not group:
            return jsonify({"error":
                            f"Group with ID {group_id} not found"}), 404

        # Check if the user is part of the group
        membership = GroupMembership.query.filter_by(
            group=group, user_id=current_user.id).first()
        if not membership:
            return jsonify({"error":
                            "You are not a member of this group"}), 404

        # Remove the user from the group
        db.session.delete(membership)
        db.session.commit()

        return jsonify({"message": "Successfully left the group"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@group_routes_bp.route(
        '/group/<string:group_id>/kick_member', methods=['POST'])
@login_required
def kick_member_from_group(group_id):
    """
    Kicks a member from a specified group.

    Args:
        group_id (str): The ID of the group to kick the member from.

    Returns:
        JSON response indicating success or failure.
    """
    try:
        # Extract the member ID to be kicked from the request body
        member_id = request.json.get('member_id')
        if not member_id:
            return jsonify({"error": "Member ID is required"}), 400

        # Check if the group exists
        group = Group.query.filter_by(id=group_id).first()
        if not group:
            return jsonify(
                {"error": f"Group with ID {group_id} not found"}), 404

        # Check if the current user is the owner of the group
        if group.owner_id != current_user.id:
            return jsonify({"error": "Unauthorized action"}), 403

        # Check if the member exists
        member = User.query.filter_by(id=member_id).first()
        if not member:
            return jsonify({"error": f"User {member_id} not found"}), 404

        # Check if the user is a member of the group
        membership = GroupMembership.query.filter_by(
                                    group=group, user_id=member_id).first()
        if not membership:
            return jsonify({"error":
                            f"User {member_id} is not a member of this group"
                            }), 404

        # Remove the member from the group
        db.session.delete(membership)

        # Commit the changes to the database
        db.session.commit()

        return jsonify({"message":
                        "User kicked from the group successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
