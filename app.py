"""
User Preferences Microservice
Handles user preference settings (language, email notification, theme, font size)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# CORS configuration
CORS(app, resources={
    r"/*": {
        "origins": os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(','),
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///user_preferences.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Database Model
class UserPreference(db.Model):
    """User preferences model"""
    __tablename__ = 'user_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False, index=True)
    language = db.Column(db.String(20), default='English', nullable=False)
    email_notification = db.Column(db.Boolean, default=True, nullable=False)
    theme = db.Column(db.String(50), default='winter', nullable=False)
    font_size = db.Column(db.String(20), default='medium', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'language': self.language,
            'email_notification': self.email_notification,
            'theme': self.theme,
            'font_size': self.font_size,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


# Default preferences
DEFAULT_PREFERENCES = {
    'language': 'English',
    'email_notification': True,
    'theme': 'winter',
    'font_size': 'medium'
}

# Valid options for validation
VALID_OPTIONS = {
    'language': ['English', 'Korean'],
    'theme': ['spring-summer', 'fall-brown', 'winter'],
    'font_size': ['small', 'medium', 'large']
}


# Helper function to validate preferences
def validate_preferences(data):
    """Validate preference data"""
    errors = []
    
    if 'language' in data and data['language'] not in VALID_OPTIONS['language']:
        errors.append(f"Invalid language. Must be one of: {', '.join(VALID_OPTIONS['language'])}")
    
    if 'email_notification' in data and not isinstance(data['email_notification'], bool):
        errors.append("email_notification must be a boolean")
    
    if 'theme' in data and data['theme'] not in VALID_OPTIONS['theme']:
        errors.append(f"Invalid theme. Must be one of: {', '.join(VALID_OPTIONS['theme'])}")
    
    if 'font_size' in data and data['font_size'] not in VALID_OPTIONS['font_size']:
        errors.append(f"Invalid font_size. Must be one of: {', '.join(VALID_OPTIONS['font_size'])}")
    
    return errors


# Routes

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'user-preferences-service',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.route('/preferences/<int:user_id>', methods=['GET'])
def get_preferences(user_id):
    """
    Get user preferences
    Returns saved preferences or default values if none exist
    """
    try:
        preference = UserPreference.query.filter_by(user_id=user_id).first()
        
        if preference:
            return jsonify({
                'success': True,
                'preferences': preference.to_dict()
            }), 200
        else:
            # Return default preferences if none exist
            return jsonify({
                'success': True,
                'preferences': {
                    'user_id': user_id,
                    **DEFAULT_PREFERENCES
                },
                'message': 'No saved preferences found. Returning defaults.'
            }), 200
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/preferences/<int:user_id>', methods=['POST', 'PUT'])
def save_preferences(user_id):
    """
    Save or update user preferences
    Creates new preferences or updates existing ones
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Validate preferences
        validation_errors = validate_preferences(data)
        if validation_errors:
            return jsonify({
                'success': False,
                'errors': validation_errors
            }), 400
        
        # Check if preferences already exist
        preference = UserPreference.query.filter_by(user_id=user_id).first()
        
        if preference:
            # Update existing preferences
            if 'language' in data:
                preference.language = data['language']
            if 'email_notification' in data:
                preference.email_notification = data['email_notification']
            if 'theme' in data:
                preference.theme = data['theme']
            if 'font_size' in data:
                preference.font_size = data['font_size']
            
            preference.updated_at = datetime.utcnow()
            message = 'Preferences updated successfully'
        else:
            # Create new preferences
            preference = UserPreference(
                user_id=user_id,
                language=data.get('language', DEFAULT_PREFERENCES['language']),
                email_notification=data.get('email_notification', DEFAULT_PREFERENCES['email_notification']),
                theme=data.get('theme', DEFAULT_PREFERENCES['theme']),
                font_size=data.get('font_size', DEFAULT_PREFERENCES['font_size'])
            )
            db.session.add(preference)
            message = 'Preferences saved successfully'
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': message,
            'preferences': preference.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/preferences/<int:user_id>', methods=['DELETE'])
def delete_preferences(user_id):
    """
    Delete user preferences (reset to defaults)
    """
    try:
        preference = UserPreference.query.filter_by(user_id=user_id).first()
        
        if preference:
            db.session.delete(preference)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Preferences deleted successfully. Defaults will be used.'
            }), 200
        else:
            return jsonify({
                'success': True,
                'message': 'No preferences found to delete. Already using defaults.'
            }), 200
            
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/preferences/<int:user_id>/reset', methods=['POST'])
def reset_preferences(user_id):
    """
    Reset user preferences to defaults
    """
    try:
        preference = UserPreference.query.filter_by(user_id=user_id).first()
        
        if preference:
            # Reset to defaults
            preference.language = DEFAULT_PREFERENCES['language']
            preference.email_notification = DEFAULT_PREFERENCES['email_notification']
            preference.theme = DEFAULT_PREFERENCES['theme']
            preference.font_size = DEFAULT_PREFERENCES['font_size']
            preference.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Preferences reset to defaults',
                'preferences': preference.to_dict()
            }), 200
        else:
            # Create with defaults
            preference = UserPreference(
                user_id=user_id,
                **DEFAULT_PREFERENCES
            )
            db.session.add(preference)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Preferences created with defaults',
                'preferences': preference.to_dict()
            }), 200
            
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/preferences/options', methods=['GET'])
def get_options():
    """
    Get all available preference options
    """
    return jsonify({
        'success': True,
        'options': VALID_OPTIONS,
        'defaults': DEFAULT_PREFERENCES
    }), 200


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


# Initialize database
with app.app_context():
    db.create_all()
    print("Database tables created successfully")


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5003))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print(f"User Preferences Service starting on port {port}")
    print(f"Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"Debug mode: {debug}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )