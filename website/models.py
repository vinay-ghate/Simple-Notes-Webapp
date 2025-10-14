from flask_login import UserMixin
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()


class DatabaseManager:
    """
    Manages MongoDB database connections and operations.
    """
    
    def __init__(self):
        """Initialize database connection."""
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client[os.getenv('DATABASE_NAME', 'notes_app')]
        self.users_collection = self.db.users
        self.notes_collection = self.db.notes
    
    def get_client(self) -> MongoClient:
        """
        Get MongoDB client instance.
        
        Returns:
            MongoClient: The MongoDB client instance
        """
        return self.client
    
    def get_database(self):
        """
        Get database instance.
        
        Returns:
            Database: The MongoDB database instance
        """
        return self.db


# Global database manager instance
db_manager = DatabaseManager()


class User(UserMixin):
    """
    User model for handling user authentication and data.
    """
    
    def __init__(self, email: str, first_name: str, password: str, _id: Optional[str] = None):
        """
        Initialize User instance.
        
        Args:
            email (str): User's email address
            first_name (str): User's first name
            password (str): User's password (should be hashed)
            _id (Optional[str]): MongoDB ObjectId as string
        """
        self.id = _id
        self.email = email
        self.first_name = first_name
        self.password = password
    
    def get_id(self) -> str:
        """
        Get user ID for Flask-Login.
        
        Returns:
            str: User ID as string
        """
        return str(self.id)
    
    def save(self) -> str:
        """
        Save user to database.
        
        Returns:
            str: The inserted user ID
        """
        user_data = {
            'email': self.email,
            'first_name': self.first_name,
            'password': self.password,
            'created_at': datetime.utcnow()
        }
        result = db_manager.users_collection.insert_one(user_data)
        self.id = str(result.inserted_id)
        return self.id
    
    @classmethod
    def find_by_email(cls, email: str) -> Optional['User']:
        """
        Find user by email address.
        
        Args:
            email (str): Email address to search for
            
        Returns:
            Optional[User]: User instance if found, None otherwise
        """
        user_data = db_manager.users_collection.find_one({'email': email})
        if user_data:
            return cls(
                email=user_data['email'],
                first_name=user_data['first_name'],
                password=user_data['password'],
                _id=str(user_data['_id'])
            )
        return None
    
    @classmethod
    def find_by_id(cls, user_id: str) -> Optional['User']:
        """
        Find user by ID.
        
        Args:
            user_id (str): User ID to search for
            
        Returns:
            Optional[User]: User instance if found, None otherwise
        """
        try:
            user_data = db_manager.users_collection.find_one({'_id': ObjectId(user_id)})
            if user_data:
                return cls(
                    email=user_data['email'],
                    first_name=user_data['first_name'],
                    password=user_data['password'],
                    _id=str(user_data['_id'])
                )
        except Exception:
            pass
        return None
    
    def get_notes(self) -> List['Note']:
        """
        Get all notes for this user.
        
        Returns:
            List[Note]: List of user's notes
        """
        return Note.find_by_user_id(self.id)


class Note:
    """
    Note model for handling note data and operations.
    """
    
    def __init__(self, data: str, user_id: str, _id: Optional[str] = None, date: Optional[datetime] = None):
        """
        Initialize Note instance.
        
        Args:
            data (str): Note content
            user_id (str): ID of the user who owns the note
            _id (Optional[str]): MongoDB ObjectId as string
            date (Optional[datetime]): Creation date, defaults to current time
        """
        self.id = _id
        self.data = data
        self.user_id = user_id
        self.date = date or datetime.utcnow()
    
    def save(self) -> str:
        """
        Save note to database.
        
        Returns:
            str: The inserted note ID
        """
        note_data = {
            'data': self.data,
            'user_id': self.user_id,
            'date': self.date
        }
        result = db_manager.notes_collection.insert_one(note_data)
        self.id = str(result.inserted_id)
        return self.id
    
    def delete(self) -> bool:
        """
        Delete note from database.
        
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        if self.id:
            try:
                result = db_manager.notes_collection.delete_one({'_id': ObjectId(self.id)})
                return result.deleted_count > 0
            except Exception:
                pass
        return False
    
    @classmethod
    def find_by_id(cls, note_id: str) -> Optional['Note']:
        """
        Find note by ID.
        
        Args:
            note_id (str): Note ID to search for
            
        Returns:
            Optional[Note]: Note instance if found, None otherwise
        """
        try:
            note_data = db_manager.notes_collection.find_one({'_id': ObjectId(note_id)})
            if note_data:
                return cls(
                    data=note_data['data'],
                    user_id=note_data['user_id'],
                    _id=str(note_data['_id']),
                    date=note_data['date']
                )
        except Exception:
            pass
        return None
    
    @classmethod
    def find_by_user_id(cls, user_id: str) -> List['Note']:
        """
        Find all notes for a specific user.
        
        Args:
            user_id (str): User ID to search for
            
        Returns:
            List[Note]: List of notes for the user
        """
        notes = []
        note_docs = db_manager.notes_collection.find({'user_id': user_id}).sort('date', -1)
        for note_data in note_docs:
            notes.append(cls(
                data=note_data['data'],
                user_id=note_data['user_id'],
                _id=str(note_data['_id']),
                date=note_data['date']
            ))
        return notes