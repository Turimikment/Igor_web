import jwt
from datetime import datetime, timedelta
from functools import wraps
from models import User
from config import Config

def create_jwt_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token required'}), 401
        user_id = verify_token(token)
        if not user_id:
            return jsonify({'message': 'Invalid or expired token'}), 401
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 401
        return f(user, *args, **kwargs)
    return decorated