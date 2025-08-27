from flask import Blueprint, jsonify, request, render_template
from models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
import re
from jwt_utils import create_jwt_token  # Добавляем импорт

auth_bp = Blueprint('auth', __name__)

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
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Токен отсутствует'}), 401
        if token.startswith('Bearer '):
            token = token[7:]
        user_id = verify_token(token)
        if not user_id:
            return jsonify({'message': 'Неверный или просроченный токен'}), 401
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'Пользователь не найден'}), 401
        return f(user, *args, **kwargs)
    return decorated