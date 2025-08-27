# routes/auth.py
from flask import Blueprint, jsonify, request, render_template
from models import User, db
from werkzeug.security import generate_password_hash
import re

auth_bp = Blueprint('auth', __name__)

def is_valid_email(email):
    return re.match(r'^[^@]+@[^@]+\.[^@]+$', email)

def is_valid_password(password):
    return len(password) >= 6  # Можно усилить: цифры, символы и т.д.

@auth_bp.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.json

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Валидация
    if not username or not email or not password:
        return jsonify({'message': 'Все поля обязательны'}), 400

    if not is_valid_email(email):
        return jsonify({'message': 'Некорректный email'}), 400

    if not is_valid_password(password):
        return jsonify({'message': 'Пароль должен быть не менее 6 символов'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Пользователь с таким логином уже существует'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Пользователь с таким email уже существует'}), 400

    # Хэшируем пароль
    hashed_password = generate_password_hash(password)

    # Создаём пользователя
    user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
        salt="",  # В реальности — генерируй соль отдельно
        is_active=True
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Регистрация успешна'}), 201