"""
Module that contains notification routes in the ChatFlow application.

Routes:
    - GET /notifications:
        Fetches notifications for the logged-in user.
        Query parameter `unread` (optional): If set to true,
            returns only unread notifications.
    - POST /notifications/<notification_id>/read:
        Marks a specific notification as read for the logged-in user.
    - DELETE /notifications/<notification_id>:
        Deletes a specific notification for the logged-in user.
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from website import db
from ..models.notification import Notification


# Define notification routes blueprint
notification_routes_bp = Blueprint('notification', __name__)


@notification_routes_bp.route('/notifications', methods=['GET'])
@login_required
def get_notifications():
    """
    Fetches notifications for the logged-in user.

    Query Parameters:
        - unread (optional): If set to 'true',
            only unread notifications are returned.

    Returns:
        - JSON response containing a list of notifications with details like:
            - id: Notification ID.
            - message: Notification message.
            - type: Notification type (e.g., 'info', 'alert').
            - is_read: Boolean indicating if the notification is read.
            - timestamp: Date and time of the notification
    """
    # Check if only unread notifications should be fetched
    unread_only = request.args.get('unread', 'false').lower() == 'true'

    # Query the database for notifications belonging to the current user
    notifications_query = Notification.query.filter_by(
        user_id=current_user.id)
    if unread_only:
        notifications_query = notifications_query.filter_by(is_read=False)

    # Order notifications by the most recent and fetch all results
    notifications = notifications_query.order_by(
        Notification.timestamp.desc()).all()

    # Return notifications in JSON format
    return jsonify([{
        'id': n.id,
        'message': n.message,
        'type': n.type,
        'is_read': n.is_read,
        'timestamp': n.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
    } for n in notifications])


@notification_routes_bp.route(
        '/notifications/<string:notification_id>/read', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    """
    Marks a notification as read for the logged-in user.

    Parameters:
        - notification_id: The ID of the notification to be marked as read.

    Returns:
        - JSON response with a success flag if the operation is completed.
        - 404 error if the notification is not found
            or doesn't belong to the user.
    """
    # Fetch the notification by ID and ensure it belongs to the current user
    notification = Notification.query.filter_by(
        id=notification_id, user_id=current_user.id).first()

    if notification:
        # Update the notification's read status
        notification.is_read = True
        db.session.commit()
        return jsonify({"success": True})

    # Return an error if the notification is not found
    return jsonify(
        {"success": False, "message": "Notification not found"}), 404


@notification_routes_bp.route(
        '/notifications/<string:notification_id>', methods=['DELETE'])
@login_required
def delete_notification(notification_id):
    """
    Deletes a specific notification for the logged-in user.

    Parameters:
        - notification_id: The unique ID of the notification to be deleted.

    Returns:
        - JSON response with a success flag if the deletion is successful.
        - 404 error if the notification is not found
            or doesn't belong to the user.
    """
    # Fetch the notification by ID
    notification = Notification.query.get(notification_id)
    if not notification or notification.user_id != current_user.id:
        # Return an error if the notification is not found or access is denied
        return jsonify(
            {'error': 'Notification not found or access denied'}), 404

    # Delete the notification and commit the changes
    db.session.delete(notification)
    db.session.commit()
    return jsonify({'success': True})
