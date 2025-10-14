# Notes App - MongoDB Version

A simple Flask web application for managing personal notes, now powered by MongoDB with improved architecture and security.

## Features

- **User Authentication**: Secure signup and login with bcrypt password hashing
- **Personal Notes**: Create and manage private notes tied to your account
- **Real-time Deletion**: Delete notes instantly with AJAX functionality
- **MongoDB Integration**: Scalable NoSQL database with proper indexing
- **Class-based Architecture**: Clean, maintainable code with docstrings
- **Environment Configuration**: Secure configuration management
- **Responsive Design**: Bootstrap-powered UI that works on all devices

## Setup Instructions

### Prerequisites

- Python 3.7+
- MongoDB Atlas account (or local MongoDB installation)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd notes-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   
   The `.env` file is already configured with your MongoDB connection string:
   ```
   MONGODB_URI=mongodb+srv://shroot:shroot@cluster0.mdsa2zb.mongodb.net/
   SECRET_KEY=hjshjhdjah kjshkjdhjs
   DATABASE_NAME=notes_app
   ```

4. **Initialize Database**
   ```bash
   python init_db.py
   ```

5. **Run the Application**
   ```bash
   python main.py
   ```

   The app will be available at `http://localhost:5000`

## Project Structure

```
├── main.py                 # Application entry point
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── website/
    ├── __init__.py        # App factory and configuration
    ├── config.py          # Configuration classes
    ├── models.py          # MongoDB models (User, Note)
    ├── auth.py            # Authentication routes and logic
    ├── views.py           # Main application routes
    ├── static/
    │   └── index.js       # Frontend JavaScript
    └── templates/         # HTML templates
        ├── base.html
        ├── home.html
        ├── login.html
        └── sign_up.html
```

## Key Improvements

### Code Architecture
- **Class-based design**: Controllers and models are organized in classes
- **Docstrings**: All methods have comprehensive docstrings
- **Type hints**: Added for better code documentation
- **Error handling**: Proper exception handling throughout

### Security
- **Password hashing**: Using bcrypt for secure password storage
- **Input validation**: Email format validation and data sanitization
- **Environment variables**: Sensitive data stored in .env file

### Database
- **MongoDB**: Replaced SQLite with MongoDB for better scalability
- **Indexes**: Automatic index creation for performance
- **Connection management**: Proper connection handling

### User Experience
- **Better error messages**: More informative user feedback
- **Input validation**: Client and server-side validation
- **Clean UI**: Simple, responsive design

## API Endpoints

- `GET /` - Home page (requires login)
- `POST /` - Create new note
- `GET /login` - Login page
- `POST /login` - Process login
- `GET /sign-up` - Registration page
- `POST /sign-up` - Process registration
- `GET /logout` - Logout user
- `POST /delete-note` - Delete note (AJAX)
- `GET /checkHealth` - Health check endpoint

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: MongoDB with PyMongo driver
- **Authentication**: Flask-Login with bcrypt password hashing
- **Frontend**: Bootstrap + jQuery for responsive UI
- **Configuration**: python-dotenv for environment management

## Usage

1. **Sign Up**: Create a new account with email and password
2. **Login**: Access your personal note dashboard
3. **Add Notes**: Use the textarea to create new notes
4. **Delete Notes**: Click the delete button to remove notes instantly

## Development

To run in development mode:
```bash
export FLASK_ENV=development
python main.py
```

For production deployment, set:
```bash
export FLASK_ENV=production
```

## Database Schema

The application uses two main collections:

### Users Collection
```javascript
{
  _id: ObjectId,
  email: String (unique),
  first_name: String,
  password: String (bcrypt hashed),
  created_at: Date
}
```

### Notes Collection
```javascript
{
  _id: ObjectId,
  data: String,
  user_id: String,
  date: Date
}
```

## Security Features

- Bcrypt password hashing
- User session management with Flask-Login
- Route protection with `@login_required` decorator
- User authorization checks for note operations
- Input validation and sanitization
- Environment-based configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.