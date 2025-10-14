from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
import bcrypt
from flask_login import login_user, login_required, logout_user, current_user
from typing import Optional, Tuple
import re

auth = Blueprint('auth', __name__)


class AuthController:
    """
    Controller class for handling authentication operations.
    """
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password (str): Plain text password
            
        Returns:
            str: Hashed password
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password (str): Plain text password
            hashed_password (str): Hashed password
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format.
        
        Args:
            email (str): Email address to validate
            
        Returns:
            bool: True if email is valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_registration_data(email: str, first_name: str, password1: str, password2: str) -> Tuple[bool, str]:
        """
        Validate user registration data.
        
        Args:
            email (str): Email address
            first_name (str): First name
            password1 (str): Password
            password2 (str): Password confirmation
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if User.find_by_email(email):
            return False, 'Email already exists.'
        elif not AuthController.validate_email(email):
            return False, 'Please enter a valid email address.'
        elif len(email) < 4:
            return False, 'Email must be at least 4 characters.'
        elif len(first_name.strip()) < 2:
            return False, 'First name must be at least 2 characters.'
        elif password1 != password2:
            return False, 'Passwords don\'t match.'
        elif len(password1) < 7:
            return False, 'Password must be at least 7 characters.'
        
        return True, ''


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.
    
    Returns:
        str: Rendered template or redirect response
    """
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Please fill in all fields.', category='error')
        else:
            user = User.find_by_email(email)
            if user:
                if AuthController.verify_password(password, user.password):
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect password, please try again.', category='error')
            else:
                flash('Email does not exist.', category='error')
    
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    """
    Handle user logout.
    
    Returns:
        Response: Redirect to login page
    """
    logout_user()
    flash('You have been logged out successfully.', category='success')
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """
    Handle user registration.
    
    Returns:
        str: Rendered template or redirect response
    """
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        first_name = request.form.get('firstName', '').strip()
        password1 = request.form.get('password1', '')
        password2 = request.form.get('password2', '')
        
        is_valid, error_message = AuthController.validate_registration_data(
            email, first_name, password1, password2
        )
        
        if not is_valid:
            flash(error_message, category='error')
        else:
            try:
                hashed_password = AuthController.hash_password(password1)
                new_user = User(
                    email=email,
                    first_name=first_name,
                    password=hashed_password
                )
                new_user.save()
                login_user(new_user, remember=True)
                flash('Account created successfully!', category='success')
                return redirect(url_for('views.home'))
            except Exception:
                flash('An error occurred while creating your account. Please try again.', category='error')
    
    return render_template("sign_up.html", user=current_user)