#!/usr/bin/env python3
"""
Database initialization script for MongoDB setup.
"""

from website.models import db_manager
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()


class DatabaseInitializer:
    """
    Handles database initialization and setup.
    """
    
    def __init__(self):
        """Initialize database connection."""
        self.db_manager = db_manager
    
    def create_indexes(self) -> None:
        """
        Create database indexes for better performance.
        """
        try:
            # Create index on email for users collection (unique)
            self.db_manager.users_collection.create_index("email", unique=True)
            print("✓ Created unique index on users.email")
            
            # Create index on user_id for notes collection
            self.db_manager.notes_collection.create_index("user_id")
            print("✓ Created index on notes.user_id")
            
            # Create index on date for notes collection (for sorting)
            self.db_manager.notes_collection.create_index("date")
            print("✓ Created index on notes.date")
            
        except Exception as e:
            print(f"✗ Error creating indexes: {e}")
    
    def test_connection(self) -> bool:
        """
        Test database connection.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Test connection by pinging the database
            self.db_manager.client.admin.command('ping')
            print("✓ MongoDB connection successful")
            return True
        except Exception as e:
            print(f"✗ MongoDB connection failed: {e}")
            return False
    
    def initialize(self) -> None:
        """
        Initialize the database with indexes and test connection.
        """
        print("Initializing MongoDB database...")
        print(f"Database: {os.getenv('DATABASE_NAME', 'notes_app')}")
        
        if self.test_connection():
            self.create_indexes()
            print("✓ Database initialization completed successfully!")
        else:
            print("✗ Database initialization failed!")


if __name__ == "__main__":
    initializer = DatabaseInitializer()
    initializer.initialize()