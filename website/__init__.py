from flask import Flask
from flask_login import LoginManager
from .config import config
import os


class AppFactory:
    """
    Factory class for creating Flask application instances.
    """
    
    @staticmethod
    def create_app(config_name: str = None) -> Flask:
        """
        Create and configure Flask application.
        
        Args:
            config_name (str): Configuration environment name
        
        Returns:
            Flask: Configured Flask application instance
        """
        if config_name is None:
            config_name = os.getenv('FLASK_ENV', 'default')
        
        app = Flask(__name__)
        app.config.from_object(config[config_name])
        
        # Register blueprints
        from .views import views
        from .auth import auth
        
        app.register_blueprint(views, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/')
        
        # Setup login manager
        AppFactory._setup_login_manager(app)
        
        return app
    
    @staticmethod
    def _setup_login_manager(app: Flask) -> None:
        """
        Configure Flask-Login for the application.
        
        Args:
            app (Flask): Flask application instance
        """
        from .models import User
        
        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.login_message = 'Please log in to access this page.'
        login_manager.login_message_category = 'info'
        login_manager.init_app(app)
        
        @login_manager.user_loader
        def load_user(user_id: str):
            """
            Load user by ID for Flask-Login.
            
            Args:
                user_id (str): User ID to load
                
            Returns:
                User: User instance if found, None otherwise
            """
            return User.find_by_id(user_id)


def create_app(config_name: str = None) -> Flask:
    """
    Create Flask application using the factory pattern.
    
    Args:
        config_name (str): Configuration environment name
    
    Returns:
        Flask: Configured Flask application instance
    """
    return AppFactory.create_app(config_name)