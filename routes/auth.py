#routes/auth.py
from flask import Blueprint, jsonify, request, render_template
from models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
import re
from jwt_utils import create_jwt_token  # Добавляем импорт

auth_bp = Blueprint('auth', __name__)

def is_valid_email(email):
    return re.match(r'^[^@]+@[^@]+\.[^@]+$', email)

def is_valid_password(password):
    return len(password) >= 6

@auth_bp.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'Все поля обязательны'}), 400

    if not is_valid_email(email):
        return jsonify({'message': 'Некорректный email'}), 400

    if not is_valid_password(password):
        return jsonify({'message': 'Пароль должен быть не менее 6 символов'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Логин занят'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email уже используется'}), 400

    hashed = generate_password_hash(password)
    user = User(username=username, email=email, password_hash=hashed, is_active=True)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Регистрация успешна'}), 201

@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        token = create_jwt_token(user.id)
        return jsonify({'access_token': token})

    return jsonify({'message': 'Неверный логин или пароль'}), 401