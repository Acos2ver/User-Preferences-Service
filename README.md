User Preferences Microservice
A microservice for managing user preference settings including language, email notifications, theme, and font size.
Features

Save/Update user preferences
Load user preferences with defaults
Reset preferences to defaults
Delete user preferences
Input validation
Performance optimized (responds within 500ms)
Docker support for easy deployment

Setup Instructions
Option 1: Traditional Setup
1. Install Dependencies
bashpip install -r requirements.txt
2. Configure Environment Variables
IMPORTANT: Never commit your .env file to version control!
Create a .env file in the root directory:
bashcp .env.example .env
Then edit .env with your configuration:
envDATABASE_URL="your_database_url_here"
PORT=your_port_number
FLASK_ENV="development_or_production"
CORS_ORIGINS="your_frontend_urls_here"
The .env file is already included in .gitignore for security.
3. Run the Service
bashpython app.py
The service will start on http://localhost:5003

Option 2: Docker Setup (Recommended)
1. Build Docker Image
bashdocker build -t user-preferences-service .
2. Run Docker Container
bashdocker run -p 5003:5003 user-preferences-service
Or run in background:
bashdocker run -d -p 5003:5003 --name user-preferences user-preferences-service
3. Using Docker Compose (Easiest)
If you have docker-compose.yml:
bash# Start service
docker-compose up

# Start in background
docker-compose up -d

# Stop service
docker-compose down
Docker Commands
bash# View logs
docker logs user-preferences

# Stop container
docker stop user-preferences

# Remove container
docker rm user-preferences

# Remove image
docker rmi user-preferences-service

API Endpoints
Health Check
httpGET /health
Response:
json{
  "status": "healthy",
  "service": "user-preferences-service",
  "timestamp": "2025-01-01T12:00:00+00:00"
}
Get User Preferences
httpGET /preferences/<user_id>
Response (if preferences exist):
json{
  "success": true,
  "preferences": {
    "id": 1,
    "user_id": 123,
    "language": "English",
    "email_notification": true,
    "theme": "winter",
    "font_size": "medium",
    "created_at": "2025-01-01T12:00:00",
    "updated_at": "2025-01-01T12:00:00"
  }
}
Response (if no preferences exist - returns defaults):
json{
  "success": true,
  "preferences": {
    "user_id": 123,
    "language": "English",
    "email_notification": true,
    "theme": "winter",
    "font_size": "medium"
  },
  "message": "No saved preferences found. Returning defaults."
}
Save/Update User Preferences
httpPOST /preferences/<user_id>
PUT /preferences/<user_id>
Request Body:
json{
  "language": "Korean",
  "email_notification": false,
  "theme": "spring-summer",
  "font_size": "large"
}
Response:
json{
  "success": true,
  "message": "Preferences saved successfully",
  "preferences": {
    "id": 1,
    "user_id": 123,
    "language": "Korean",
    "email_notification": false,
    "theme": "spring-summer",
    "font_size": "large",
    "created_at": "2025-01-01T12:00:00",
    "updated_at": "2025-01-01T12:00:00"
  }
}
Reset Preferences to Defaults
httpPOST /preferences/<user_id>/reset
Response:
json{
  "success": true,
  "message": "Preferences reset to defaults",
  "preferences": {
    "id": 1,
    "user_id": 123,
    "language": "English",
    "email_notification": true,
    "theme": "winter",
    "font_size": "medium",
    "created_at": "2025-01-01T12:00:00",
    "updated_at": "2025-01-01T12:00:00"
  }
}
Delete User Preferences
httpDELETE /preferences/<user_id>
Response:
json{
  "success": true,
  "message": "Preferences deleted successfully. Defaults will be used."
}
Get Available Options
httpGET /preferences/options
Response:
json{
  "success": true,
  "options": {
    "language": ["English", "Korean"],
    "theme": ["spring-summer", "fall-brown", "winter"],
    "font_size": ["small", "medium", "large"]
  },
  "defaults": {
    "language": "English",
    "email_notification": true,
    "theme": "winter",
    "font_size": "medium"
  }
}
Database Schema
UserPreference Model
ColumnTypeDescriptionidIntegerPrimary keyuser_idIntegerUser ID (unique, indexed)languageString(20)Language preference (English/Korean)email_notificationBooleanEmail notification settingthemeString(50)Theme preferencefont_sizeString(20)Font size preferencecreated_atDateTimeCreation timestampupdated_atDateTimeLast update timestamp
Valid Options
Language

English
Korean

Theme

spring-summer
fall-brown
winter (default)

Font Size

small
medium (default)
large

Email Notification

true (default)
false

Performance Requirements
The service responds within 500ms for GET requests to maintain a responsive user experience.
Error Handling
All endpoints return appropriate HTTP status codes:

200 - Success
400 - Bad Request (validation errors)
404 - Not Found
500 - Internal Server Error

Error Response Format:
json{
  "success": false,
  "error": "Error message here"
}
Testing
Run Test Script
bashpython test.py
Testing with cURL
Get preferences:
bashcurl http://localhost:5003/preferences/123
Save preferences:
bashcurl -X POST http://localhost:5003/preferences/123 \
  -H "Content-Type: application/json" \
  -d '{
    "language": "Korean",
    "email_notification": false,
    "theme": "spring-summer",
    "font_size": "large"
  }'
Reset to defaults:
bashcurl -X POST http://localhost:5003/preferences/123/reset
Delete preferences:
bashcurl -X DELETE http://localhost:5003/preferences/123
Integration with Frontend
Update your frontend api.js to include:
javascriptconst PREFERENCES_API_URL = 
  import.meta.env.VITE_PREFERENCES_API || 'http://localhost:5003'

// Get user preferences
export async function getPreferencesApi(userId) {
  const res = await fetch(`${PREFERENCES_API_URL}/preferences/${userId}`)
  const data = await res.json()
  if (!res.ok) throw new Error(data.error || 'Failed to get preferences')
  return data
}

// Save user preferences
export async function savePreferencesApi(userId, preferences) {
  const res = await fetch(`${PREFERENCES_API_URL}/preferences/${userId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(preferences)
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.error || 'Failed to save preferences')
  return data
}

// Reset preferences
export async function resetPreferencesApi(userId) {
  const res = await fetch(`${PREFERENCES_API_URL}/preferences/${userId}/reset`, {
    method: 'POST'
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.error || 'Failed to reset preferences')
  return data
}
Project Structure
user-preferences/
├── app.py                 # Main application
├── test.py               # Test script
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
├── Dockerfile           # Docker configuration
├── .dockerignore        # Docker ignore rules
└── README.md            # This file
Technology Stack

Flask - Web framework
SQLAlchemy - ORM for database operations
SQLite - Default database (configurable)
Flask-CORS - CORS support
Python-dotenv - Environment variable management

License
MIT
## Authors

- **Olivia Choi** - Oregon State University
- **Tiffany Gorseth** - Collaborator
