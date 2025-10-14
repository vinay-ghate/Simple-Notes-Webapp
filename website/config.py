"""
Configuration settings for the Flask application.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Base configuration class with common settings.
    """
    
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key-change-in-production')
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'notes_app')
    
    # Security settings
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


class DevelopmentConfig(Config):
    """
    Development configuration with debug settings.
    """
    
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """
    Production configuration with security optimizations.
    """
    
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """
    Testing configuration for unit tests.
    """
    
    DEBUG = True
    TESTING = True
    DATABASE_NAME = 'notes_app_test'


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}