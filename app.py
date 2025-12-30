from flask import Flask, request, jsonify
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Import Supabase - handle version compatibility
try:
    from supabase import create_client, Client
except ImportError:
    try:
        from supabase.client import create_client, Client
    except ImportError:
        create_client = None
        Client = None

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Supabase configuration
# Try environment variables first, then fallback to hardcoded (for testing only)
SUPABASE_URL = os.getenv('SUPABASE_URL') or os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY') or os.environ.get('SUPABASE_KEY')

# HARDCODED FALLBACK (ONLY FOR TESTING - NOT RECOMMENDED FOR PRODUCTION)
# Remove these after confirming environment variables work!
if not SUPABASE_URL:
    SUPABASE_URL = 'https://huyzlryubollexkuykgd.supabase.co'
if not SUPABASE_KEY:
    SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh1eXpscnl1Ym9sbGV4a3V5a2dkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjcwOTE2NTUsImV4cCI6MjA4MjY2NzY1NX0.709TKB1MZbLXLb210KSe4nj4cHhgwK9jDZWhdFOL6fY'

# Initialize Supabase client
supabase: Optional[Client] = None
USE_SUPABASE = False
SUPABASE_INIT_ERROR = None

if SUPABASE_URL and SUPABASE_KEY:
    try:
        # Create Supabase client - use the already imported create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Test connection by trying to query (this will fail if tables don't exist)
        try:
            result = supabase.table('users').select('id').limit(1).execute()
            USE_SUPABASE = True
            print(f"✅ Supabase initialized successfully")
        except Exception as table_error:
            # If it's a table not found error, that's okay - we'll create it
            error_str = str(table_error).lower()
            if 'relation' in error_str and 'does not exist' in error_str:
                USE_SUPABASE = False
                SUPABASE_INIT_ERROR = f"Tables don't exist. Run SQL setup script: {str(table_error)}"
                print(f"⚠️ Supabase connected but tables don't exist: {table_error}")
                print("Make sure you've run the SQL setup script in Supabase!")
            else:
                # Other error - might be permissions or connection
                USE_SUPABASE = False
                SUPABASE_INIT_ERROR = str(table_error)
                print(f"⚠️ Supabase connection issue: {table_error}")
    except Exception as e:
        USE_SUPABASE = False
        SUPABASE_INIT_ERROR = str(e)
        print(f"❌ Warning: Could not initialize Supabase: {e}")
        print("Falling back to JSON file storage")
else:
    print(f"⚠️ Supabase not configured:")
    print(f"   SUPABASE_URL: {'Set' if SUPABASE_URL else 'NOT SET'}")
    print(f"   SUPABASE_KEY: {'Set' if SUPABASE_KEY else 'NOT SET'}")
    print("Falling back to JSON file storage")
DB_FILE = 'whatsapp_messages.json'
USERS_DB_FILE = 'users.json'

# ============================================================================
# SUPABASE FUNCTIONS
# ============================================================================

def save_message_to_supabase(data: Dict[Any, Any]) -> None:
    """Save message to Supabase messages table"""
    if not supabase:
        raise Exception("Supabase not configured")
    
    # Add timestamp if not present
    if 'timestamp' not in data:
        data['timestamp'] = datetime.now().isoformat()
    
    # Insert into messages table
    supabase.table('messages').insert({
        'data': json.dumps(data),
        'timestamp': data['timestamp']
    }).execute()

def get_messages_from_supabase() -> list:
    """Get all messages from Supabase"""
    if not supabase:
        raise Exception("Supabase not configured")
    
    response = supabase.table('messages').select('*').order('timestamp', desc=True).execute()
    messages = []
    for row in response.data:
        try:
            msg_data = json.loads(row['data']) if isinstance(row['data'], str) else row['data']
            msg_data['id'] = row['id']
            messages.append(msg_data)
        except:
            messages.append(row)
    return messages

def get_message_by_id_from_supabase(message_id: int) -> Optional[dict]:
    """Get message by ID from Supabase"""
    if not supabase:
        raise Exception("Supabase not configured")
    
    response = supabase.table('messages').select('*').eq('id', message_id).execute()
    if response.data:
        row = response.data[0]
        try:
            msg_data = json.loads(row['data']) if isinstance(row['data'], str) else row['data']
            msg_data['id'] = row['id']
            return msg_data
        except:
            return row
    return None

def get_user_from_supabase(phone: str) -> Optional[dict]:
    """Get user by phone from Supabase"""
    if not supabase:
        raise Exception("Supabase not configured")
    
    response = supabase.table('users').select('*').eq('phone', phone).execute()
    if response.data:
        user = response.data[0]
        # Parse wishlist if it's a string
        if isinstance(user.get('wishlist'), str):
            try:
                user['wishlist'] = json.loads(user['wishlist'])
            except:
                user['wishlist'] = []
        return user
    return None

def save_user_to_supabase(user_data: Dict[Any, Any]) -> dict:
    """Save or update user in Supabase"""
    if not supabase:
        raise Exception("Supabase not configured")
    
    phone = user_data['phone']
    
    # Check if user exists
    existing = get_user_from_supabase(phone)
    
    # Prepare data for Supabase
    db_data = {
        'phone': phone,
        'parent_name': user_data['parent_name'],
        'child_name': user_data['child_name'],
        'wishlist': json.dumps(user_data.get('wishlist', [])),
        'updated_at': datetime.now().isoformat()
    }
    
    if existing:
        # Update existing user
        db_data['created_at'] = existing.get('created_at', datetime.now().isoformat())
        response = supabase.table('users').update(db_data).eq('phone', phone).execute()
    else:
        # Create new user
        db_data['created_at'] = datetime.now().isoformat()
        response = supabase.table('users').insert(db_data).execute()
    
    # Return the saved user
    saved_user = response.data[0] if isinstance(response.data, list) else response.data
    if isinstance(saved_user.get('wishlist'), str):
        try:
            saved_user['wishlist'] = json.loads(saved_user['wishlist'])
        except:
            saved_user['wishlist'] = []
    
    return saved_user

def get_all_users_from_supabase() -> dict:
    """Get all users from Supabase"""
    if not supabase:
        raise Exception("Supabase not configured")
    
    response = supabase.table('users').select('*').execute()
    users = {}
    for row in response.data:
        phone = row['phone']
        # Parse wishlist if it's a string
        if isinstance(row.get('wishlist'), str):
            try:
                row['wishlist'] = json.loads(row['wishlist'])
            except:
                row['wishlist'] = []
        users[phone] = row
    return users

# ============================================================================
# JSON FALLBACK FUNCTIONS (for local development without Supabase)
# ============================================================================

def load_database() -> list:
    """Load messages from JSON database (fallback)"""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_to_database(data: Dict[Any, Any]) -> None:
    """Save message to JSON database (fallback)"""
    messages = load_database()
    
    if 'timestamp' not in data:
        data['timestamp'] = datetime.now().isoformat()
    
    if 'id' not in data:
        data['id'] = len(messages) + 1
    
    messages.append(data)
    
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)

def load_users() -> dict:
    """Load users from JSON database (fallback)"""
    if os.path.exists(USERS_DB_FILE):
        try:
            with open(USERS_DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_users(users: dict) -> None:
    """Save users to JSON database (fallback)"""
    with open(USERS_DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

def get_user_by_phone(phone: str) -> dict:
    """Get user by phone number (fallback)"""
    users = load_users()
    return users.get(phone, None)

# ============================================================================
# API ROUTES
# ============================================================================

@app.route('/webhook', methods=['POST'])
def whatsapp_webhook():
    """Webhook endpoint to receive WhatsApp messages"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No data received'
            }), 400
        
        # Store the data
        if USE_SUPABASE:
            save_message_to_supabase(data)
        else:
            save_to_database(data)
        
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
    """Webhook verification endpoint"""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
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
    """Retrieve all stored messages"""
    try:
        if USE_SUPABASE:
            messages = get_messages_from_supabase()
        else:
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
    """Retrieve a specific message by ID"""
    try:
        if USE_SUPABASE:
            message = get_message_by_id_from_supabase(message_id)
        else:
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
    """Check if user exists by phone number"""
    try:
        data = request.get_json()
        
        if not data or 'phone' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Phone number is required'
            }), 400
        
        phone = data['phone']
        
        if USE_SUPABASE:
            user = get_user_from_supabase(phone)
        else:
            users = load_users()
            user = users.get(phone)
        
        if user:
            return jsonify({
                'exists': True,
                'parent_name': user.get('parent_name', ''),
                'child_name': user.get('child_name', ''),
                'wishlist': user.get('wishlist', [])
            }), 200
        else:
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
    """Save or update user information"""
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
        
        # Prepare user data
        user_data = {
            'phone': phone,
            'parent_name': data['parent_name'],
            'child_name': data['child_name'],
            'wishlist': data.get('wishlist', [])
        }
        
        if USE_SUPABASE:
            try:
                saved_user = save_user_to_supabase(user_data)
            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': f'Supabase error: {str(e)}',
                    'fallback_used': False
                }), 500
        else:
            # Fallback to JSON (will fail on Vercel)
            try:
                users = load_users()
                existing = users.get(phone, {})
                user_data['created_at'] = existing.get('created_at', datetime.now().isoformat())
                user_data['updated_at'] = datetime.now().isoformat()
                users[phone] = user_data
                save_users(users)
                saved_user = user_data
            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': f'JSON storage failed (read-only filesystem): {str(e)}. Please configure Supabase environment variables in Vercel.',
                    'hint': 'Add SUPABASE_URL and SUPABASE_KEY to Vercel environment variables and redeploy'
                }), 500
        
        return jsonify({
            'status': 'success',
            'message': 'User saved successfully',
            'user': saved_user
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/users', methods=['GET'])
def get_all_users():
    """Retrieve all users from database"""
    try:
        if USE_SUPABASE:
            users = get_all_users_from_supabase()
        else:
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
    """Retrieve a specific user by phone number"""
    try:
        if USE_SUPABASE:
            user = get_user_from_supabase(phone)
        else:
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
        'database': 'Supabase' if USE_SUPABASE else 'JSON Files',
        'supabase_configured': USE_SUPABASE,
        'supabase_url_set': bool(SUPABASE_URL),
        'supabase_key_set': bool(SUPABASE_KEY)
    }), 200

@app.route('/debug', methods=['GET'])
def debug_info():
    """Debug endpoint to check configuration"""
    return jsonify({
        'supabase_url': SUPABASE_URL[:30] + '...' if SUPABASE_URL and len(SUPABASE_URL) > 30 else SUPABASE_URL,
        'supabase_key': SUPABASE_KEY[:30] + '...' if SUPABASE_KEY and len(SUPABASE_KEY) > 30 else SUPABASE_KEY,
        'supabase_configured': USE_SUPABASE,
        'supabase_client': 'initialized' if supabase else 'not initialized',
        'init_error': SUPABASE_INIT_ERROR,
        'environment_vars': {
            'SUPABASE_URL': 'SET' if os.getenv('SUPABASE_URL') or os.environ.get('SUPABASE_URL') else 'NOT SET (using hardcoded)',
            'SUPABASE_KEY': 'SET' if os.getenv('SUPABASE_KEY') or os.environ.get('SUPABASE_KEY') else 'NOT SET (using hardcoded)'
        },
        'hint': 'If init_error shows table error, run SQL setup script in Supabase'
    }), 200

if __name__ == '__main__':
    # Initialize JSON databases if not using Supabase
    if not USE_SUPABASE:
        if not os.path.exists(DB_FILE):
            with open(DB_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)
        
        if not os.path.exists(USERS_DB_FILE):
            with open(USERS_DB_FILE, 'w', encoding='utf-8') as f:
                json.dump({}, f)
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

