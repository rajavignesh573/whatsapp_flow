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
if not SUPABASE_URL:
    SUPABASE_URL = 'https://huyzlryubollexkuykgd.supabase.co'
if not SUPABASE_KEY:
    SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh1eXpscnl1Ym9sbGV4a3V5a2dkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjcwOTE2NTUsImV4cCI6MjA4MjY2NzY1NX0.709TKB1MZbLXLb210KSe4nj4cHhgwK9jDZWhdFOL6fY'

# Initialize Supabase client - REQUIRED
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set. Add them to environment variables.")

if not create_client:
    raise RuntimeError("Supabase library not installed. Run: pip install supabase")

supabase: Optional[Client] = None
SUPABASE_INIT_ERROR = None

try:
    # Create Supabase client
    # Handle potential proxy argument issues in serverless environments
    # Set NO_PROXY to prevent httpx from trying to use proxy settings
    import os
    os.environ.setdefault('NO_PROXY', '*')
    os.environ.setdefault('no_proxy', '*')
    # Also disable proxy for httpx specifically
    os.environ.setdefault('HTTP_PROXY', '')
    os.environ.setdefault('HTTPS_PROXY', '')
    os.environ.setdefault('http_proxy', '')
    os.environ.setdefault('https_proxy', '')
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except TypeError as type_error:
        # If there's a type error with proxy argument, it's likely a version compatibility issue
        # Try to work around it by using the client with explicit options
        error_msg = str(type_error).lower()
        if 'proxy' in error_msg:
            # The issue is likely that httpx (used by supabase) is trying to pass proxy
            # but the Client doesn't accept it. Try to patch httpx or use alternative initialization
            try:
                # Try patching httpx to remove proxy from kwargs
                import httpx
                original_init = httpx.Client.__init__
                def patched_init(self, *args, **kwargs):
                    kwargs.pop('proxy', None)
                    kwargs.pop('proxies', None)
                    return original_init(self, *args, **kwargs)
                httpx.Client.__init__ = patched_init
                
                # Now try creating the client again
                supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            except Exception as patch_error:
                # If patching fails, try using the client module directly
                try:
                    from supabase.client import Client, ClientOptions
                    options = ClientOptions(
                        auto_refresh_token=True,
                        persist_session=False
                    )
                    supabase = Client(SUPABASE_URL, SUPABASE_KEY, options)
                except Exception as alt_error:
                    # If that fails, log the error
                    print(f"⚠️ Alternative initialization failed: {alt_error}")
                    raise type_error  # Re-raise original error
        else:
            raise
    
    # Test connection by trying to query (this will fail if tables don't exist)
    try:
        result = supabase.table('users').select('id').limit(1).execute()
        print(f"✅ Supabase initialized successfully")
    except Exception as table_error:
        # If it's a table not found error, warn but allow app to start
        error_str = str(table_error).lower()
        if 'relation' in error_str and 'does not exist' in error_str:
            SUPABASE_INIT_ERROR = f"Tables don't exist. Run SQL setup script: {str(table_error)}"
            print(f"⚠️ Supabase connected but tables don't exist: {table_error}")
            print("Make sure you've run the SQL setup script in Supabase!")
        else:
            SUPABASE_INIT_ERROR = str(table_error)
            print(f"⚠️ Supabase connection issue: {table_error}")
except Exception as e:
    SUPABASE_INIT_ERROR = str(e)
    print(f"❌ Failed to initialize Supabase: {e}")
    # Don't raise error - allow app to start but mark as uninitialized
    # This is important for serverless environments where initialization might fail
    supabase = None

if not supabase:
    print("⚠️ WARNING: Supabase client not initialized. Some endpoints may not work.")

# ============================================================================
# SUPABASE FUNCTIONS
# ============================================================================

def save_message(data: Dict[Any, Any]) -> None:
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

def get_messages() -> list:
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

def get_message_by_id(message_id: int) -> Optional[dict]:
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

def get_user(phone: str) -> Optional[dict]:
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

def save_user(user_data: Dict[Any, Any]) -> dict:
    """Save or update user in Supabase"""
    if not supabase:
        raise Exception("Supabase not configured")
    
    phone = user_data['phone']
    
    # Check if user exists
    existing = get_user(phone)
    
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

def get_all_users() -> dict:
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

def get_menu_items() -> list:
    """Get all menu items from Supabase"""
    if not supabase:
        raise Exception("Supabase not configured")
    
    response = supabase.table('menu_items').select('*').order('display_order', desc=False).execute()
    menu_items = []
    for row in response.data:
        menu_items.append({
            'id': row['id'],
            'title': row['title']
        })
    return menu_items

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
        
        # Store the data in Supabase
        save_message(data)
        
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
def get_messages_endpoint():
    """Retrieve all stored messages"""
    try:
        messages = get_messages()
        
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
def get_message_endpoint(message_id: int):
    """Retrieve a specific message by ID"""
    try:
        message = get_message_by_id(message_id)
        
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
        user = get_user(phone)
        
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
def save_user_endpoint():
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
        
        # Save to Supabase
        saved_user = save_user(user_data)
        
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
def get_all_users_endpoint():
    """Retrieve all users from database"""
    try:
        users = get_all_users()
        
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
def get_user_endpoint(phone: str):
    """Retrieve a specific user by phone number"""
    try:
        user = get_user(phone)
        
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
        'database': 'Supabase',
        'supabase_configured': supabase is not None,
        'supabase_url_set': bool(SUPABASE_URL),
        'supabase_key_set': bool(SUPABASE_KEY),
        'init_error': SUPABASE_INIT_ERROR
    }), 200

@app.route('/debug', methods=['GET'])
def debug_info():
    """Debug endpoint to check configuration"""
    return jsonify({
        'supabase_url': SUPABASE_URL[:30] + '...' if SUPABASE_URL and len(SUPABASE_URL) > 30 else SUPABASE_URL,
        'supabase_key': SUPABASE_KEY[:30] + '...' if SUPABASE_KEY and len(SUPABASE_KEY) > 30 else SUPABASE_KEY,
        'supabase_configured': supabase is not None,
        'supabase_client': 'initialized' if supabase else 'not initialized',
        'init_error': SUPABASE_INIT_ERROR,
        'environment_vars': {
            'SUPABASE_URL': 'SET' if os.getenv('SUPABASE_URL') or os.environ.get('SUPABASE_URL') else 'NOT SET (using hardcoded)',
            'SUPABASE_KEY': 'SET' if os.getenv('SUPABASE_KEY') or os.environ.get('SUPABASE_KEY') else 'NOT SET (using hardcoded)'
        },
        'hint': 'If init_error shows table error, run SQL setup script in Supabase'
    }), 200

@app.route('/menu', methods=['GET'])
def get_menu_endpoint():
    """Retrieve all menu items"""
    try:
        menu_items = get_menu_items()
        
        return jsonify({
            'status': 'success',
            'count': len(menu_items),
            'menu': menu_items
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
