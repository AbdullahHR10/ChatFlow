"""
Module that contains the friendship routes for the ChatFlow application.

Routes:
    - POST /add_friend: Sends a friend request to another user.
        Validates if the user exists, prevents sending requests to oneself,
        checks if the recipient allows requests,
            and handles existing friendships.
    - POST /cancel_request/<friendship_id>: Cancels a pending friend request.
        Ensures the request belongs to the current user and is still pending.
    - POST /accept_request/<friendship_id>: Accepts a pending friend request.
        Validates the friendship request and updates the status to accepted.
        Sends notifications to both the requesting user and the receiver.
    - POST /reject_friend_request/<friendship_id>:
        Rejects a pending friend request.
            Validates if the friendship exists,
            ensures the current user is the recipient of the request,
    - POST /remove_friend/<friendship_id>:
            Removes a friend from the user's friend list.
    - GET /friends: Displays the list of all users excluding the current user
    - GET /api/friends: Returns a JSON response
        containing a list of the current user's friends,
        excluding those with whom the user has an existing chat.
"""
from flask import (
    Blueprint, request, redirect, url_for, flash, jsonify, render_template)
from flask_login import login_required, current_user
from ..models.friendship import Friendship, FriendshipStatus
from ..models.conversation import Conversation
from ..models.notification import Notification
from ..models.user import User
from website import db, socketio

friendship_routes_bp = Blueprint('friendship', __name__)


@friendship_routes_bp.route('/add_friend', methods=['POST'])
@login_required
def add_friend():
    """
    Adds a friend by sending a friend request to another user.
    Validates if the friend ID exists, checks if the user can send the request,
    and handles various friendship statuses (pending, accepted, blocked).

    Returns:
        Redirects to the dashboard with an appropriate flash message.
    """
    # Get the friend ID from the request form
    friend_id = request.form.get('friend_id')

    # If friend ID is not provided, show an error and redirect
    if not friend_id:
        flash("Friend ID is required", "error")
        return redirect(url_for('main_routes_bp.dashboard'))

    # Find the friend user by the provided ID
    friend = User.query.filter_by(friend_id=friend_id).first()

    # If the user does not exist, show an error and redirect
    if not friend:
        flash("User not found", "error")
        return redirect(url_for('main_routes_bp.dashboard'))

    # Prevent sending a friend request to oneself
    if friend.id == current_user.id:
        flash("You cannot send a friend request to yourself", "error")
        return redirect(url_for('main_routes_bp.dashboard'))

    # Check if the friend allows friend requests
    if not friend.allow_friend_requests:
        flash("This user doesn't allow friend requests", "error")
        return redirect(url_for('main_routes_bp.dashboard'))

    # Check if there is an existing friendship with the user
    existing_friendship = Friendship.query.filter(
        ((Friendship.user_id_1 == current_user.id) &
         (Friendship.user_id_2 == friend.id)) |
        ((Friendship.user_id_1 == friend.id) &
         (Friendship.user_id_2 == current_user.id))
    ).first()

    # Handle different friendship statuses
    if existing_friendship:
        if existing_friendship.status == FriendshipStatus.PENDING.value:
            flash("Friend request already sent.", "warning")
        elif existing_friendship.status == FriendshipStatus.ACCEPTED.value:
            flash("You are already friends.", "info")
        elif existing_friendship.status == FriendshipStatus.BLOCKED.value:
            flash("This user has blocked you.", "error")
        return redirect(url_for('main_routes_bp.dashboard'))

    # Create a new friendship entry in the database
    new_friendship = Friendship(user_id_1=current_user.id,
                                user_id_2=friend.id)
    db.session.add(new_friendship)
    db.session.commit()

    # Send a notification to the user about the friend request
    notification_message = (
        f"{current_user.name} "
        "has sent you a friend request."
    )
    notification = Notification(user_id=friend.id,
                                message=notification_message,
                                type='friend_request', is_read=False
                                )
    db.session.add(notification)
    db.session.commit()

    # Emit a real-time notification to the friend
    socketio.emit('new_notification',
                  {'message': notification_message, 'type': 'friend_request'},
                  room=f"user_{friend.id}")

    # Show a success message and redirect to the dashboard
    flash("Friend request sent successfully", "success")
    return redirect(url_for('main_routes_bp.dashboard'))


@friendship_routes_bp.route(
        '/cancel_request/<string:friendship_id>', methods=['POST'])
@login_required
def cancel_request(friendship_id):
    """
    Cancels a pending friend request.
        Ensures the request exists and belongs to the current user
            before deletion.

    Args:
        friendship_id (str): The ID of the friendship to cancel.

    Returns:
        Redirects to the dashboard with an appropriate flash message.
    """
    # Find the friendship by ID and check if the status is "pending"
    friendship = Friendship.query.filter_by(
        id=friendship_id, status=FriendshipStatus.PENDING.value).first()

    # If the friendship does not exist or is not pending,
    # show an error and redirect
    if not friendship:
        flash("Friend request not found.", "danger")
        return redirect(url_for('main_routes_bp.dashboard'))

    # Ensure the current user is the one who sent the friend request
    if friendship.user_id_1 != current_user.id:
        flash("You cannot cancel this friend request.", "danger")
        return redirect(url_for('main_routes_bp.dashboard'))

    # Delete the pending friend request from the database
    db.session.delete(friendship)
    db.session.commit()

    # Show a success message and redirect to the dashboard
    flash("Friend request has been canceled.", "success")
    return redirect(url_for('main_routes_bp.dashboard'))


@friendship_routes_bp.route(
        '/accept_friend_request/<string:friendship_id>', methods=['POST'])
@login_required
def accept_request(friendship_id):
    """
    Accepts a pending friend request.
    Validates that the friend request exists
        and that the current user is authorized to accept it.
    Sends a notification to the user who sent the request,
        and emits a real-time notification.

    Args:
        friendship_id (str): The ID of the friendship request to accept.

    Returns:
        Redirects to the dashboard with an appropriate flash message.
    """
    # Retrieve the friendship request from the database by ID
    friendship = Friendship.query.get(friendship_id)

    # If the friendship does not exist, show an error and redirect
    if not friendship:
        flash("Friend request not found.", "danger")
        return redirect(url_for('main_routes_bp.dashboard'))

    # Ensure the current user is the one receiving the friend request
    if friendship.user_id_2 != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for('main_routes_bp.dashboard'))

    # Call the method to accept the friend request
    friendship.accept_request()

    # Prepare the notification message
    # to inform the sender that the request was accepted
    notification_message = (
        f"{current_user.name} has accepted your friend request."
        )

    # Create a new notification for the sender
    notification = Notification(
        user_id=friendship.user_id_1,
        message=notification_message,
        type='friend_request',
        is_read=False
    )

    # Add the notification to the database and commit the changes
    db.session.add(notification)
    db.session.commit()

    # Emit a real-time notification to the sender using Socket.IO
    socketio.emit('new_notification',
                  {'message': notification_message, 'type': 'friend_request'},
                  room=f"user_{friendship.user_id_1}")

    # Show a success message and redirect to the dashboard
    flash("Friend request accepted.", "success")
    return redirect(url_for('main_routes_bp.dashboard'))


@friendship_routes_bp.route(
        '/reject_friend_request/<string:friendship_id>', methods=['POST'])
@login_required
def reject_request(friendship_id):
    """
    Rejects a pending friend request.
    Validates that the friend request exists and
        that the current user is authorized to reject it.

    Args:
        friendship_id (str): The ID of the friendship request to reject.

    Returns:
        Redirects to the dashboard with an appropriate flash message.
    """
    # Retrieve the friendship request from the database by ID
    friendship = Friendship.query.get(friendship_id)

    # If the friendship does not exist, show an error and redirect
    if not friendship:
        flash("Friend request not found.", "danger")
        return redirect(url_for('main_routes_bp.dashboard'))

    # Ensure the current user is the one receiving the friend request
    if friendship.user_id_2 != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for('main_routes_bp.dashboard'))

    # Call the method to reject the friend request
    friendship.decline_request()

    # Show a success message and redirect to the dashboard
    flash("Friend request rejected.", "success")
    return redirect(url_for('main_routes_bp.dashboard'))


@friendship_routes_bp.route(
        '/remove_friend/<string:friendship_id>', methods=['POST'])
@login_required
def remove_friend(friendship_id):
    """
    Removes a friend from the user's friend list.
    Validates that the friendship exists and
        the current user is authorized to remove the friend.

    Args:
        friendship_id (str): The ID of the friendship to remove.

    Returns:
        Redirects to the dashboard with an appropriate flash message.
    """
    # Retrieve the friendship from the database by its ID
    friendship = Friendship.query.get(friendship_id)

    # If the friendship does not exist, show an error and redirect
    if not friendship:
        flash("Friendship not found.", "danger")
        return redirect(url_for('main_routes_bp.dashboard'))

    # Ensure the current user is involved in the friendship
    if (friendship.user_id_1 != current_user.id
       and friendship.user_id_2 != current_user.id):
        flash("Unauthorized action.", "danger")
        return redirect(url_for('main_routes_bp.dashboard'))

    # Call the method to remove the friendship
    friendship.remove_friendship()

    # Show a success message and redirect to the dashboard
    flash("Friendship removed.", "success")
    return redirect(url_for('main_routes_bp.dashboard'))


@friendship_routes_bp.route('/friends')
def friends():
    """
    Displays the list of friends, incoming friend requests
        and outgoing friend requests for the currently logged-in user.

    Retrieves all users excluding the current user, the accepted friendships,
    and the pending incoming and outgoing friend requests.

    Returns:
        Renders the 'friends.html' template with the relevant data.
    """
    # Retrieve the current logged-in user
    user = current_user

    # Retrieve all users excluding the current user
    all_users = User.query.filter(User.id != current_user.id).all()

    # Retrieve all accepted friendships
    friendships = Friendship.query.filter(
        (Friendship.user_1 == user) | (Friendship.user_2 == user),
        Friendship.status == 'accepted'
    ).all()

    # Retrieve all incoming friend requests
    incoming_requests = Friendship.query.filter_by(
        user_2=user, status='pending').all()

    # Retrieve all outgoing friend requests
    outgoing_requests = Friendship.query.filter_by(
        user_1=user, status='pending').all()

    # Render the friends template and pass the relevant data
    return render_template(
        'friends.html',
        all_users=all_users,
        friendships=friendships,
        incoming_requests=incoming_requests,
        outgoing_requests=outgoing_requests
    )


@friendship_routes_bp.route('/api/friends', methods=['GET'])
@login_required
def get_friends():
    """
    Retrieves the list of friends for the currently logged-in user.
        excludes friends who already have an existing chat with the user.

    Returns:
        A JSON response containing the list of friends.
        If an error occurs, a 500 response with the error message is returned.
    """
    try:
        # Get the current logged-in user's ID
        user_id = current_user.id

        # Check if the 'exclude_chats' query parameter is set to true
        exclude_chats = request.args.get(
            'exclude_chats', 'true').lower() == 'true'

        # Get the list of friend IDs
        friends_ids = Friendship.get_friends(user_id)
        if not friends_ids:
            return jsonify({"error": "No friends found."}), 404

        # Fetch user data for the friends' IDs
        friends = User.query.filter(User.id.in_(friends_ids)).all()

        # Set to store IDs of friends with whom
        # the user has existing private conversations
        existing_chat_ids = set()

        # If exclude_chats is enabled, fetch existing chats with friends
        if exclude_chats:
            existing_chats = Conversation.query.filter(
                (Conversation.user1_id == user_id) |
                (Conversation.user2_id == user_id)
            ).all()
            for chat in existing_chats:
                # Add the other user to the set of existing chat IDs
                if chat.user1_id == user_id:
                    existing_chat_ids.add(chat.user2_id)
                elif chat.user2_id == user_id:
                    existing_chat_ids.add(chat.user1_id)

        # Filter friends by excluding those with
        # whom the user has an existing chat
        if exclude_chats:
            filtered_friends = [
                friend for friend in friends if friend.id
                not in existing_chat_ids
            ]
        else:
            filtered_friends = friends

        # Return the list of friends as a JSON response
        return jsonify({
            'friends': [{
                'id': friend.id,
                'name': friend.name,
                'profile_picture':
                (f'/static/profile_pics/{friend.profile_picture}'
                    if friend.profile_picture
                    else '/static/profile_pics/default.png')
            } for friend in filtered_friends]
        })

    except Exception as e:
        # Log the error and return a 500 response with the error message
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500
