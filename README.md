# User Preferences Microservice

A microservice for managing user preference settings including language, email notifications, theme, and font size.

## Features

- Save/Update user preferences
- Load user preferences with defaults
- Reset preferences to defaults
- Delete user preferences
- Input validation
- Performance optimized (responds within 500ms)
- Docker support for easy deployment

## Setup Instructions

### Option 1: Traditional Setup

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Configure Environment Variables

**IMPORTANT:** Never commit your `.env` file to version control!

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Then edit `.env` with your configuration:

```env
DATABASE_URL="your_database_url_here"
PORT=your_port_number
FLASK_ENV="development_or_production"
CORS_ORIGINS="your_frontend_urls_here"
```

The `.env` file is already included in `.gitignore` for security.

#### 3. Run the Service

```bash
python app.py
```

The service will start on http://localhost:5003

---

### Option 2: Docker Setup (Recommended)

#### 1. Build Docker Image

```bash
docker build -t user-preferences-service .
```

#### 2. Run Docker Container

```bash
docker run -p 5003:5003 user-preferences-service
```

Or run in background:

```bash
docker run -d -p 5003:5003 --name user-preferences user-preferences-service
```

#### 3. Using Docker Compose (Easiest)

If you have `docker-compose.yml`:

```bash
# Start service
docker-compose up

# Start in background
docker-compose up -d

# Stop service
docker-compose down
```

#### Docker Commands

```bash
# View logs
docker logs user-preferences

# Stop container
docker stop user-preferences

# Remove container
docker rm user-preferences

# Remove image
docker rmi user-preferences-service
```

---

## API Endpoints

### Health Check

```http
GET /health
```

**Response:**

```json
{
  "status": "healthy",
  "service": "user-preferences-service",
  "timestamp": "2025-01-01T12:00:00+00:00"
}
```

### Get User Preferences

```http
GET /preferences/<user_id>
```

**Response (if preferences exist):**

```json
{
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
```

**Response (if no preferences exist - returns defaults):**

```json
{
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
```

### Save/Update User Preferences

```http
POST /preferences/<user_id>
PUT /preferences/<user_id>
```

**Request Body:**

```json
{
  "language": "Korean",
  "email_notification": false,
  "theme": "spring-summer",
  "font_size": "large"
}
```

**Response:**

```json
{
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
```

### Reset Preferences to Defaults

```http
POST /preferences/<user_id>/reset
```

**Response:**

```json
{
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
```

### Delete User Preferences

```http
DELETE /preferences/<user_id>
```

**Response:**

```json
{
  "success": true,
  "message": "Preferences deleted successfully. Defaults will be used."
}
```

### Get Available Options

```http
GET /preferences/options
```

**Response:**

```json
{
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
```
### UML Diagram
<img width="938" height="1098" alt="image" src="https://github.com/user-attachments/assets/81f7ad45-d4da-4163-9073-a4ac9f997e1b" />

### Database Schema
CREATE TABLE user_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    language VARCHAR(20) NOT NULL DEFAULT 'English',
    email_notification BOOLEAN NOT NULL DEFAULT 1,
    theme VARCHAR(50) NOT NULL DEFAULT 'winter',
    font_size VARCHAR(20) NOT NULL DEFAULT 'medium',
    created_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    updated_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);
CREATE INDEX idx_user_preferences_user_id 
ON user_preferences (user_id);

### UserPreference Model

| Column             | Type        | Description                            |
|--------------------|-------------|----------------------------------------|
| id                 | Integer     | Primary key                            |
| user_id            | Integer     | User ID (unique, indexed)              |
| language           | String(20)  | Language preference (English/Korean)   |
| email_notification | Boolean     | Email notification setting             |
| theme              | String(50)  | Theme preference                       |
| font_size          | String(20)  | Font size preference                   |
| created_at         | DateTime    | Creation timestamp                     |
| updated_at         | DateTime    | Last update timestamp                  |

## Valid Options

### Language
- English
- Korean

### Theme
- spring-summer
- fall-brown
- winter (default)

### Font Size
- small
- medium (default)
- large

### Email Notification
- true (default)
- false

## Performance Requirements

The service responds within 500ms for GET requests to maintain a responsive user experience.

## Error Handling

All endpoints return appropriate HTTP status codes:

- **200** - Success
- **400** - Bad Request (validation errors)
- **404** - Not Found
- **500** - Internal Server Error

**Error Response Format:**

```json
{
  "success": false,
  "error": "Error message here"
}
```

## Testing

### Run Test Script

```bash
python test.py
```

### Testing with cURL

**Get preferences:**

```bash
curl http://localhost:5003/preferences/123
```

**Save preferences:**

```bash
curl -X POST http://localhost:5003/preferences/123 \
  -H "Content-Type: application/json" \
  -d '{
    "language": "Korean",
    "email_notification": false,
    "theme": "spring-summer",
    "font_size": "large"
  }'
```

**Reset to defaults:**

```bash
curl -X POST http://localhost:5003/preferences/123/reset
```

**Delete preferences:**

```bash
curl -X DELETE http://localhost:5003/preferences/123
```

## Integration with Frontend

Update your frontend `api.js` to include:

```javascript
const PREFERENCES_API_URL = 
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
```

## Project Structure

```
user-preferences/
├── app.py                 # Main application
├── test.py               # Test script
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
├── Dockerfile           # Docker configuration
├── .dockerignore        # Docker ignore rules
└── README.md            # This file
```

## Technology Stack

- **Flask** - Web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Default database (configurable)
- **Flask-CORS** - CORS support
- **Python-dotenv** - Environment variable management

## License

MIT

## Authors

- **Olivia Choi** - Oregon State University
- **Tiffany Gorseth** - Collaborator
