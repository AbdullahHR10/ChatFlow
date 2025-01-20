"""
Module for handling authentication routes in the ChatFlow app.

Routes:
    - GET /authentication: Renders login page,
        redirects if already authenticated.
    - POST /authentication: Processes login form, checks credentials.
    - GET /logout: Logs the user out and redirects to login.
    - GET /signup: Renders sign-up page, redirects if already authenticated.
    - POST /signup: Processes sign-up form, validates data, creates user.
"""
from flask import (Blueprint, render_template, request,
                   flash, redirect, url_for)
from flask_login import login_user, login_required, logout_user, current_user
from ..models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from website import db

# Define authentication blueprint
authentication = Blueprint('authentication', __name__)


@authentication.route('/authentication', methods=['GET', 'POST'])
def login():
    """ Logs the user in. """
    # If the user is already authenticated, redirect them to the home page
    if current_user.is_authenticated:
        return redirect(url_for('main_routes_bp.home'))

    # If the request method is POST, process the login form submission
    if request.method == 'POST':
        # Retrieve the phone number and password entered by the user
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')

        # Check if the user exists by looking up the phone number
        user = User.query.filter_by(phone_number=phone_number).first()
        if user:
            # If the password matches, log the user in
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', 'success')
                # Log the user in with the 'remember me' option
                login_user(user, remember=True)
                # Redirect to home page
                return redirect(url_for('main_routes_bp.home'))
            else:
                # Flash error if the password is incorrect
                flash('Incorrect Password.', 'error')
        else:
            # Flash error if the user does not exist
            flash('User does not exist.', 'error')
    # Render the login page with the current user context
    return render_template('authentication.html', user=current_user)


@authentication.route('/logout')
@login_required
def logout():
    """ Logs the user out. """
    # Log the user out and clear the session
    logout_user()
    # Flash a success message indicating the user has been logged out
    flash('Logged out successfully!', 'success')
    # Redirect the user to the login page after logging out
    return redirect(url_for('authentication.login'))


@authentication.route('/signup', methods=['GET', 'POST'])
def sign_up():
    """ Signs the user up. """
    # If the user is already authenticated (logged in),
    # redirect to the home page
    if current_user.is_authenticated:
        return redirect(url_for('main_routes_bp.home'))

    if request.method == 'POST':
        # Get the submitted form data for name,
        # phone number, password, and confirm password
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        try:
            # Check if the phone number or name already exists before
            # creating a new user
            user_by_phone_number = User.query.filter_by(
                phone_number=phone_number).first()

            # Validate the name and password
            if len(name) < 1:
                flash("Name must be at least 1 character.", 'error')
            elif len(name) > 25:
                flash("Name must be less than 25 characters.", 'error')
            elif user_by_phone_number:
                flash('Phone number is already in use.', 'error')
            elif len(password) < 6:
                flash("Password must be at least 6 characters.", 'error')
            elif confirm_password != password:
                flash("Passwords don't match.", 'error')
            else:
                # Only create the user if all checks pass
                new_user = User(
                    name=name,
                    phone_number=phone_number,
                    # Hash the password
                    password=generate_password_hash(password,
                                                    method='pbkdf2:sha256')
                )

                # Add the new user to the database and commit the changes
                db.session.add(new_user)
                db.session.commit()

                # Log the new user in and flash a success message
                login_user(new_user, remember=True)
                flash("Account created!", 'success')

                # Redirect to the home page after successful sign-up
                return redirect(url_for('main_routes_bp.home'))
        except Exception as e:
            # If an error occurs during user creation, flash an error message
            flash(f'An error occurred. Please try again: {e}', 'error')

    # Render the sign-up page (authentication.html)
    # if the method is GET or if there is an error
    return render_template('authentication.html', user=current_user)
