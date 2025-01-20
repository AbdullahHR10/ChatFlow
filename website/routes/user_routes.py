"""
Module that contains user routes in the ChatFlow application.

Routes:
    - GET /api/current_user_id:
        Returns the ID of the currently authenticated user.
    - POST /upload_profile_picture:
        Handles the uploading and updating of the user's profile picture.
    - POST /update_profile:
        Allows users to update various profile details such as username, bio,
            birthdate, and social media links.
"""

from flask import (Blueprint, redirect, flash,
                   url_for, jsonify, request, current_app)
from flask_login import login_required, current_user

from ..utils import allowed_file
from website import db
from website.models.user import User

import os
import datetime

# Define main_routes blueprint
user_routes_bp = Blueprint('user_routes_bp', __name__)


@user_routes_bp.route('/api/current_user_id', methods=['GET'])
@login_required
def get_current_user_id():
    """
    Get the ID of the currently authenticated user.

    Requirements:
        - User must be logged in.

    Returns:
        JSON: A response containing the user's ID in the format:
              {"user_id": <current_user.id>}
    """
    return jsonify({'user_id': current_user.id})


@user_routes_bp.route('/upload_profile_picture', methods=['POST'])
def upload_profile_picture():
    """
    Handle uploading and updating the user's profile picture.

    This endpoint processes a file upload for the user's profile picture.
    The uploaded file is validated for allowed file types,
        saved to the server, and the user's profile picture
            is updated in the database.

    Returns:
        Redirect: Redirects the user to
            the appropriate page with a status message.
                  - On success: Redirects to the dashboard
                    with a success message.
                  - On failure: Redirects to the profile page or dashboard
                    with an error message.
    """
    # Check if the 'file' key exists in the request
    if 'file' not in request.files:
        # Redirect to dashboard with an error message if no file part is found
        return redirect(url_for('main_routes_bp.dashboard',
                                message="No file part"))

    # Retrieve the uploaded file
    file = request.files['file']

    # Check if the file has no filename
    if file.filename == '':
        # Redirect to dashboard with an error message if no file is selected
        return redirect(url_for('main_routes_bp.dashboard',
                                message="No selected file"))

    # Validate the file and ensure it has an allowed extension
    if file and allowed_file(file.filename):
        # Create a unique filename
        # using the user's ID and the original file extension
        filename = f"{current_user.id}{os.path.splitext(file.filename)[1]}"
        # Define the file path for saving the profile picture
        file_path = os.path.join(
            current_app.config['PROFILE_PICS_UPLOAD_FOLDER'], filename)
        # Save the file to the server
        file.save(file_path)
        # Update the user's profile picture in the database
        current_user.profile_picture = filename
        db.session.commit()
        # Redirect to the dashboard with a success message
        return redirect(url_for(
            'main_routes_bp.dashboard',
            message="Profile picture updated successfully"))
    else:
        # Redirect to the dashboard with an error message
        # if the file type is invalid
        return redirect(url_for('routes.dashboard',
                                message="Invalid file type"))


@user_routes_bp.route('/update_profile', methods=['POST'])
def update_profile():
    """
    Update user profile details.

    This endpoint allows users to update various profile fields dynamically
    based on the provided field name and value.

    Request Body:
        JSON: {
            "field": <field_name>,  # The name of the profile field to update.
            "value": <value>        # The new value for the specified field.
        }

    Returns:
        JSON:
            - Success: {"success": True}
            - Failure: {"success": False, "message": <error_message>}
              with an appropriate HTTP status code
                (e.g., 400 for bad requests).

    Supported Fields:
        - username
        - bio
        - birthdate (format: YYYY-MM-DD)
        - location
        - job_title
        - facebook_link (must start with "https://www.facebook.com/")
        - discord_id
        - github_link (must start with "https://github.com/")
        - youtube_link (must start with "https://www.youtube.com/")
        - website_link

    Notes:
        - Validation is performed for specific fields
            like `birthdate` and social media links.
        - If the `field` is invalid or unrecognized,
            the request will fail with an error message.
    """
    # Parse the incoming JSON data
    data = request.json
    # Get the field to update
    field = data.get('field')
    # Get the new value for the field
    value = data.get('value')

    # Handle updates for different fields
    # ensuring no leading/trailing whitespace
    if field == 'name':
        # Update the name
        current_user.name = value.strip()
    elif field == 'bio':
        # Update the bio
        current_user.bio = value.strip()
    elif field == 'birthdate':
        # Validate and update the birthdate
        try:
            value = datetime.datetime.strptime(value.strip(), "%Y-%m-%d").date()
            current_user.birthdate = value
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Invalid birthdate format. Use YYYY-MM-DD.'}), 400
    elif field == 'location':
        # Update the location
        current_user.location = value.strip()
    elif field == 'job_title':
        # Update the job title
        current_user.job_title = value.strip()
    elif field == 'facebook_link':
        # Validate and update the Facebook link
        if value and not value.strip().startswith(
                "https://www.facebook.com/"):
            return jsonify({'success': False,
                            'message': 'Invalid Facebook link.'}), 400
        current_user.facebook_link = value
    elif field == 'discord_id':
        # Update the Discord ID
        current_user.discord_id = value
    elif field == 'github_link':
        # Validate and update the GitHub link
        if value and not value.strip().startswith("https://github.com/"):
            return jsonify({'success': False,
                            'message': 'Invalid GitHub link.'}), 400
        current_user.github_link = value
    elif field == 'youtube_link':
        # Validate and update the YouTube link
        if value and not value.strip().startswith("https://www.youtube.com/"):
            return jsonify({'success': False,
                            'message': 'Invalid YouTube link.'}), 400
        current_user.youtube_link = value
    elif field == 'website_link':
        # Update the website link
        current_user.website_link = value
    else:
        # Return an error for unsupported or invalid fields
        return jsonify({'success': False, 'message': 'Invalid field'}), 400
    db.session.commit()
    return jsonify({'success': True})


@user_routes_bp.route('/update-privacy-settings', methods=['POST'])
def update_privacy_settings():
    """
    Updates user privacy settings.

    Returns:
        Redirects the user to the dashboard page.
    """
    # Get the current user
    user = User.query.get(current_user.id)
    
    # List of privacy-related fields to update
    privacy_fields = [
        'phone_number_is_private',
        'last_seen_is_private',
        'bio_is_private',
        'birthdate_is_private',
        'location_is_private',
        'job_title_is_private',
        'allow_friend_requests'
    ]
    
    # Update the privacy fields
    for field in privacy_fields:
        # Check if the field is in the form and handle checkbox status
        value = request.form.get(field) == 'on'  # If it's 'on', set to True; otherwise False
        setattr(user, field, value)
    
    try:
        db.session.commit()  # Commit the changes to the database
        flash("Privacy settings updated.", "success")
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        flash("There was an error updating your privacy settings.", "danger")
        print(f"Error: {e}")
    
    return redirect(url_for('main_routes_bp.dashboard'))
