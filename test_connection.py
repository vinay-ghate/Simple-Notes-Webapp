#!/usr/bin/env python3
"""
Simple script to test MongoDB connection and basic operations.
"""

from website.models import User, Note, db_manager
from website.auth import AuthController
from dotenv import load_dotenv

load_dotenv()


def test_connection():
    """Test basic MongoDB connection and operations."""
    print("Testing MongoDB connection...")
    
    try:
        # Test connection
        db_manager.client.admin.command('ping')
        print("✓ MongoDB connection successful")
        
        # Test user creation
        print("\nTesting user operations...")
        test_email = "test@example.com"
        
        # Clean up any existing test user
        existing_user = User.find_by_email(test_email)
        if existing_user:
            db_manager.users_collection.delete_one({'email': test_email})
            print("✓ Cleaned up existing test user")
        
        # Create test user
        hashed_password = AuthController.hash_password("testpassword123")
        test_user = User(
            email=test_email,
            first_name="Test",
            password=hashed_password
        )
        user_id = test_user.save()
        print(f"✓ Created test user with ID: {user_id}")
        
        # Test user retrieval
        retrieved_user = User.find_by_email(test_email)
        if retrieved_user:
            print(f"✓ Retrieved user: {retrieved_user.first_name}")
        
        # Test password verification
        if AuthController.verify_password("testpassword123", retrieved_user.password):
            print("✓ Password verification successful")
        
        # Test note creation
        print("\nTesting note operations...")
        test_note = Note(
            data="This is a test note",
            user_id=user_id
        )
        note_id = test_note.save()
        print(f"✓ Created test note with ID: {note_id}")
        
        # Test note retrieval
        user_notes = Note.find_by_user_id(user_id)
        print(f"✓ Retrieved {len(user_notes)} notes for user")
        
        # Test note deletion
        if user_notes:
            if user_notes[0].delete():
                print("✓ Note deletion successful")
        
        # Clean up test user
        db_manager.users_collection.delete_one({'email': test_email})
        print("✓ Cleaned up test user")
        
        print("\n🎉 All tests passed! Your MongoDB setup is working correctly.")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        print("\n❌ Tests failed. Please check your MongoDB connection and configuration.")


if __name__ == "__main__":
    test_connection()