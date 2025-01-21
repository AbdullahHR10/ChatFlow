"""
Module that contains the main routes for the ChatFlow application.

Routes:
    - GET /home: Determines the appropriate page for the user
        (dashboard or landing page).
    - GET /welcome: Renders the landing page for new or unauthenticated users.
    - GET /notifications: Displays a list of notifications
        for the authenticated user.
    - GET /settings: Renders the settings main page
        for the authenticated user.
    - GET /settings/<section>: Renders a specific settings section page
        based on the section parameter
            (e.g., profile, privacy, notifications, etc.).
    - GET /dashboard: Displays the dashboard page for the authenticated user.
        Retrieves the user's conversations, groups, notifications, and more.
"""
from flask import (Blueprint, render_template,
                   redirect, url_for, session)
from flask_login import login_required, current_user

from ..models.user import User
from ..models.conversation import Conversation
from ..models.notification import Notification
from ..models.group import Group, GroupMembership

# Define main_routes blueprint
main_routes_bp = Blueprint('main_routes_bp', __name__)


@main_routes_bp.route('/')
def home():
    """
    Home page route that determines the appropriate page for the user.

    - If the user is authenticated, redirects to the dashboard.
    - If the user is not authenticated, redirects to the login page.

    Returns:
        Response: A redirect to either the dashboard
            or the login page depending on the user's authentication status.
    """
    if current_user.is_authenticated:
        # Render dashboard for logged-in users
        return redirect(url_for('main_routes_bp.dashboard'))
    else:
        # Render the landing page for new users
        return redirect(url_for('main_routes_bp.welcome'))


@main_routes_bp.route('/welcome')
def welcome():
    """
    Landing page route that directs the user to the landing page

    - For authenticated users,
        the navigation bar includes a logout button.
    - For unauthenticated users,
        the navigation bar includes login and signup buttons.

    Returns:
        Response: The rendered landing page template.
    """
    # Render the landing page
    return render_template('landing_page.html')


@main_routes_bp.route('/notifications')
@login_required
def notifications():
    """
    Displays the notifications page for authenticated users.

    - Fetches all notifications for the currently authenticated user,
        ordered by timestamp
    - in descending order. The notifications are passed to the template
        for display.

    Returns:
        Response: The rendered notifications template with the
            user's notifications.
    """
    # Fetch all notifications for the current user, ordered by the most recent
    notifications = (
        Notification.query
        .filter_by(user_id=current_user.id)
        .order_by(Notification.timestamp.desc())
        .all()
    )
    # Render the notifications page
    return render_template('notifications.html', notifications=notifications)


@main_routes_bp.route('/settings')
@login_required
def settings():
    """
    Settings page route that renders the settings template.

    - This route is accessible only by authenticated users.
    - It renders the settings page where users can update their profile,
      preferences, and other account settings.

    Returns:
        Response: The rendered settings page template.
    """
    # Render the settings page
    return render_template('settings/settings.html')


@main_routes_bp.route('/settings/<section>')
@login_required
def settings_section(section):
    """
    Settings section page route that renders the specified settings template.

    - This route allows users to view different sections of their settings.
    - It dynamically renders the template based on the section
        passed in the URL.
    - If the section is valid, the corresponding settings page is shown.
    - If the section is invalid, a 404 error is returned.

    Args:
        section (str): The section of settings to display
            (e.g., 'profile-settings', 'privacy-settings').

    Returns:
        Response: The rendered template for the specific settings sectio
            or a 404 error if the section is not found.
    """
    # Define all available settings templates
    templates = {
        'profile-settings': 'settings/profile_settings.html',
        'privacy-settings': 'settings/privacy_settings.html',
        'appearance-settings': 'settings/appearance_settings.html',
    }
    # Retrieve the template for the given section
    template = templates.get(section)

    # If the section is found, render the corresponding template
    if template:
        return render_template(template, user=current_user)

    # If the section is not valid, return a 404 error
    return "Section not found", 404


@main_routes_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """
    Dashboard route for authenticated users.

    This route serves the dashboard page for logged-in users.
    - The user's theme preference is retrieved from the session
        (default is 'dark').
    - If the user is not authenticated, they are redirected to the login page.

    Returns:
        Response: The rendered dashboard page
            or a redirect to the login page if not authenticated.
    """
    # Get the user's theme preference from the session, default is 'dark'
    theme = session.get('theme', 'dark')

    # If the user is not authenticated, redirect to the login page
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    # Retrieve all individual conversations where the user is involved
    individual_conversations = Conversation.query.filter(
        ((Conversation.user1_id == current_user.id) |
            (Conversation.user2_id == current_user.id)) &
        (Conversation.type == 'private_chat')
    ).all()

    # Retrieve all groups the user is a member of or owns
    groups = Group.query.filter(
        (Group.owner_id == current_user.id) |
        (Group.group_members.any(GroupMembership.user_id == current_user.id))
    ).all()
    # Initialize an empty list to store chat data
    private_chats = []
    for conv in individual_conversations:
        # Retrieve the friend involved in this conversation
        friend = User.query.get(
            conv.user2_id
            if conv.user1_id == current_user.id
            else conv.user1_id
        )

        # Get the last message and its timestamp if available
        last_message = conv.last_message
        if conv.last_message_date:
            last_message_date = conv.last_message_date.strftime(
                '%Y-%m-%d %H:%M')
        else:
            last_message_date = "N/A"

        # Prepare the chat data, including user info and message details
        chat_data = {
            # Conversation ID
            'id': (conv.id),

            # Friend's username or "Unknown" if not available
            'name': (friend.name if friend else "Unknown"),

            # Friend's phone number or privacy status
            'phone_number': (
                friend.phone_number if friend and friend.phone_number and
                not friend.phone_number_is_private else
                "Private" if friend and friend.phone_number_is_private else
                "Not set"
            ),

            # Friend's bio or "No bio available" if not set
            'bio': (
                friend.bio if friend and friend.bio and
                not friend.bio_is_private else "Private"
                if friend and friend.bio_is_private
                else "No bio available"
            ),

            # Friend's birthdate or privacy status
            'birthdate': (friend.birthdate.strftime('%d %B %Y')
                          if friend and friend.birthdate and
                          not friend.birthdate_is_private else 'Private'
                          if friend and friend.birthdate_is_private
                          else "Not set"),

            # Friend's location or privacy status
            'location': (
                friend.location if friend and friend.location and
                not friend.location_is_private else
                "Private" if friend and friend.location_is_private
                else "Not set"
            ),

            # Friend's job title or privacy status
            'job_title': (
                friend.job_title if friend and friend.job_title and
                not friend.job_title_is_private else "Private" if
                friend and friend.job_title_is_private else "Not set"
            ),

            # Friend's Facebook link or None
            'facebook_link': (
                friend.facebook_link if friend and friend.facebook_link
                else None
            ),

            # Friend's Discord ID or None
            'discord_id': (
                friend.discord_id if friend and friend.discord_id
                else None),

            # Friend's YouTube link or None
            'youtube_link': (
                friend.youtube_link if friend
                and friend.youtube_link
                else None),

            # Friend's GitHub link or None
            'github_link': (
                friend.github_link if
                friend and friend.github_link
                else None),

            # Friend's website link or None
            'website_link': (
                friend.website_link if
                friend and friend.website_link
                else None),

            # Profile picture URL (default if not set)
            'profile_picture_url': url_for(
                'static',
                filename=f"profile_pics/{friend.profile_picture}"
                if friend and
                friend.profile_picture
                else 'profile_pics/default.png'
            ) if friend else url_for('static',
                                     filename='profile_pics/default.png'),

            # Last message text or default if none
            'last_message': (last_message
                             if last_message
                             else "No messages yet"),

            # Last message timestamp or "N/A" if not set
            'last_message_date': (last_message_date
                                  if last_message_date
                                  else "N/A"),

            # Count of unread messages for the current user
            'unread_messages': (
                len([msg for msg in conv.messages
                    if not msg.is_read and
                    msg.receiver_id == current_user.id])
                if conv.messages
                else 0
            ),

            # Friend's online/offline status
            'status': friend.status if friend else 'offline',

            # Last seen timestamp or "N/A" if private or not available
            'last_seen': (
                friend.last_seen.strftime('%d %B %Y, %H:%M') if friend and
                friend.last_seen and not friend.last_seen_is_private
                else 'N/A'
            ),

            # ID of the other user in the conversation
            'receiver_id': conv.user2_id if conv.user1_id == current_user.id
            else conv.user1_id,
        }

        # Append the chat data to the list
        private_chats.append(chat_data)

    # Fetch notifications for the authenticated user
    notifications = Notification.query.filter_by(
        user_id=current_user.id).order_by(Notification.timestamp.desc()).all()

    # Count unread notifications for the user
    unread_notifications = Notification.query.filter_by(
        user_id=current_user.id, is_read=False).count()

    # Retrieve all users except the currently logged-in user
    users = User.query.filter(User.id != current_user.id).all()

    # Render the dashboard page with the chat, group, user,
    # and notification data
    return render_template('dashboard.html',
                           private_chats=private_chats,
                           groups=groups,
                           users=users,
                           current_user_id=current_user.id,
                           theme=theme,
                           notifications=notifications,
                           unread_notifications=unread_notifications)
