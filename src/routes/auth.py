from datetime import datetime
from flask import Blueprint, jsonify, request, session
from src.models.user import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Admin login endpoint"""
    try:
        data = request.json
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password required'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if user and user.check_password(data['password']):
            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Store user info in session
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            
            return jsonify({
                'message': 'Login successful',
                'user': user.to_dict()
            })
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Admin logout endpoint"""
    try:
        session.clear()
        return jsonify({'message': 'Logout successful'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/check-auth', methods=['GET'])
def check_auth():
    """Check if user is authenticated"""
    try:
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
            if user:
                return jsonify({
                    'authenticated': True,
                    'user': user.to_dict()
                })
        
        return jsonify({'authenticated': False}), 401
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/create-admin', methods=['POST'])
def create_admin():
    """Create initial admin user (only if no users exist)"""
    try:
        # Check if any users already exist
        if User.query.count() > 0:
            return jsonify({'error': 'Admin user already exists'}), 400
        
        data = request.json
        
        if not data or not all(k in data for k in ['username', 'email', 'password']):
            return jsonify({'error': 'Username, email, and password required'}), 400
        
        # Create admin user
        admin = User.create_admin_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        
        db.session.add(admin)
        db.session.commit()
        
        return jsonify({
            'message': 'Admin user created successfully',
            'user': admin.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def require_auth(f):
    """Decorator to require authentication for admin routes"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

