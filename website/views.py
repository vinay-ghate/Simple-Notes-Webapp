from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
import json
from typing import Dict, Any

views = Blueprint('views', __name__)


class NotesController:
    """
    Controller class for handling note-related operations.
    """
    
    @staticmethod
    def create_note(note_content: str, user_id: str) -> bool:
        """
        Create a new note for the user.
        
        Args:
            note_content (str): Content of the note
            user_id (str): ID of the user creating the note
            
        Returns:
            bool: True if note was created successfully, False otherwise
        """
        if len(note_content.strip()) < 1:
            return False
        
        try:
            new_note = Note(data=note_content.strip(), user_id=user_id)
            new_note.save()
            return True
        except Exception:
            return False
    
    @staticmethod
    def delete_note(note_id: str, user_id: str) -> bool:
        """
        Delete a note if it belongs to the user.
        
        Args:
            note_id (str): ID of the note to delete
            user_id (str): ID of the user requesting deletion
            
        Returns:
            bool: True if note was deleted successfully, False otherwise
        """
        note = Note.find_by_id(note_id)
        if note and note.user_id == user_id:
            return note.delete()
        return False


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """
    Home page route that displays user notes and handles note creation.
    
    Returns:
        str: Rendered HTML template
    """
    if request.method == 'POST':
        note_content = request.form.get('note', '').strip()
        
        if not note_content:
            flash('Note cannot be empty!', category='error')
        elif len(note_content) < 1:
            flash('Note is too short!', category='error')
        else:
            if NotesController.create_note(note_content, current_user.id):
                flash('Note added successfully!', category='success')
            else:
                flash('Failed to add note. Please try again.', category='error')
    
    # Get user's notes for display
    user_notes = Note.find_by_user_id(current_user.id)
    return render_template("home.html", user=current_user, notes=user_notes)


@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    """
    API endpoint for deleting notes via AJAX.
    
    Returns:
        Dict[str, Any]: JSON response
    """
    try:
        note_data = json.loads(request.data)
        note_id = note_data.get('noteId')
        
        if not note_id:
            return jsonify({'error': 'Note ID is required'}), 400
        
        if NotesController.delete_note(note_id, current_user.id):
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Failed to delete note'}), 400
            
    except (json.JSONDecodeError, KeyError):
        return jsonify({'error': 'Invalid request data'}), 400
    except Exception:
        return jsonify({'error': 'Internal server error'}), 500


@views.route('/checkHealth', methods=['GET'])
def check_health() -> Dict[str, str]:
    """
    Health check endpoint for monitoring application status.
    
    Returns:
        Dict[str, str]: Status information
    """
    return {"Status": "Live", "Service": "Notes App"}


