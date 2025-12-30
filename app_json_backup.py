from flask import Flask, request, jsonify
import json
import os
from datetime import datetime
from typing import Dict, Any

app = Flask(__name__)

# JSON database files
DB_FILE = 'whatsapp_messages.json'
USERS_DB_FILE = 'users.json'

def load_database() -> list:
    """Load messages from JSON database"""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_to_database(data: Dict[Any, Any]) -> None:
    """Save message to JSON database"""
    messages = load_database()
    
    # Add timestamp if not present
    if 'timestamp' not in data:
        data['timestamp'] = datetime.now().isoformat()
    
    # Add unique ID if not present
    if 'id' not in data:
        data['id'] = len(messages) + 1
    
    messages.append(data)
    
    # Save to JSON file
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)

def load_users() -> dict:
    """Load users from JSON database"""
    if os.path.exists(USERS_DB_FILE):
        try:
            with open(USERS_DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_users(users: dict) -> None:
    """Save users to JSON database"""
    with open(USERS_DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

def get_user_by_phone(phone: str) -> dict:
    """Get user by phone number"""
    users = load_users()
    return users.get(phone, None)

@app.route('/webhook', methods=['POST'])
def whatsapp_webhook():
    """
    Webhook endpoint to receive WhatsApp messages
    Accepts POST requests from WhatsApp API
    """
    try:
        # Get the incoming data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No data received'
            }), 400
        
        # Store the data in JSON database
        save_to_database(data)
        
        # Return success response (WhatsApp expects 200 OK)
        return jsonify({
            'status': 'success',
            'message': 'Message received and stored',
            'received_at': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """
    Webhook verification endpoint (for WhatsApp webhook setup)
    WhatsApp may send GET requests to verify the webhook
    """
    # WhatsApp verification parameters
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    # You can set your verify token in environment variable
    verify_token = os.getenv('WHATSAPP_VERIFY_TOKEN', 'your_verify_token_here')
    
    if mode == 'subscribe' and token == verify_token:
        return challenge, 200
    else:
        return jsonify({
            'status': 'error',
            'message': 'Verification failed'
        }), 403

@app.route('/messages', methods=['GET'])
def get_messages():
    """
    Retrieve all stored messages from JSON database
    """
    try:
        messages = load_database()
        return jsonify({
            'status': 'success',
            'count': len(messages),
            'messages': messages
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/messages/<int:message_id>', methods=['GET'])
def get_message(message_id: int):
    """
    Retrieve a specific message by ID
    """
    try:
        messages = load_database()
        message = next((m for m in messages if m.get('id') == message_id), None)
        
        if message:
            return jsonify({
                'status': 'success',
                'message': message
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Message not found'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/check-or-create-user', methods=['POST'])
def check_or_create_user():
    """
    Check if user exists by phone number
    Used by Kapso flow to determine if user is new or existing
    """
    try:
        data = request.get_json()
        
        if not data or 'phone' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Phone number is required'
            }), 400
        
        phone = data['phone']
        users = load_users()
        
        # Check if user exists
        if phone in users:
            user = users[phone]
            return jsonify({
                'exists': True,
                'parent_name': user.get('parent_name', ''),
                'child_name': user.get('child_name', ''),
                'wishlist': user.get('wishlist', [])
            }), 200
        else:
            # User doesn't exist
            return jsonify({
                'exists': False
            }), 200
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/save-user', methods=['POST'])
def save_user():
    """
    Save or update user information
    Used by Kapso flow after onboarding
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No data received'
            }), 400
        
        # Validate required fields
        required_fields = ['user', 'parent_name', 'child_name']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'status': 'error',
                    'message': f'{field} is required'
                }), 400
        
        phone = data['user']
        users = load_users()
        
        # Create or update user
        user_data = {
            'phone': phone,
            'parent_name': data['parent_name'],
            'child_name': data['child_name'],
            'wishlist': data.get('wishlist', []),
            'created_at': users.get(phone, {}).get('created_at', datetime.now().isoformat()),
            'updated_at': datetime.now().isoformat()
        }
        
        users[phone] = user_data
        save_users(users)
        
        return jsonify({
            'status': 'success',
            'message': 'User saved successfully',
            'user': user_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/users', methods=['GET'])
def get_all_users():
    """
    Retrieve all users from database
    """
    try:
        users = load_users()
        return jsonify({
            'status': 'success',
            'count': len(users),
            'users': users
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/users/<phone>', methods=['GET'])
def get_user(phone: str):
    """
    Retrieve a specific user by phone number
    """
    try:
        user = get_user_by_phone(phone)
        if user:
            return jsonify({
                'status': 'success',
                'user': user
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'WhatsApp Webhook API',
        'database_file': DB_FILE,
        'users_database_file': USERS_DB_FILE
    }), 200

if __name__ == '__main__':
    # Initialize empty databases if they don't exist
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
    
    if not os.path.exists(USERS_DB_FILE):
        with open(USERS_DB_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f)
    
    # Run the Flask app
    # Use PORT environment variable for cloud deployment (Render, Railway, etc.)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

