from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from config import Config
from models import db
from routes.products import products_bp
from routes.favorites import favorites_bp
from auth import token_required
import jwt

app = Flask(__name__)
app.config.from_object(Config)

# Инициализация
db.init_app(app)
swagger = Swagger(app)

# Регистрация роутов
app.register_blueprint(products_bp, url_prefix='/api')
app.register_blueprint(favorites_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/api/login', methods=['POST'])
def login_api():
    data = request.json
    # Пример проверки (в реальности — хэш пароля)
    if data.get('username') == 'admin' and data.get('password') == 'admin':
        token = create_jwt_token(1)  # В реальности — по ID пользователя
        return jsonify({'access_token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
@token_required
def logout(current_user):
    # Удаление токена из БД (опционально)
    return jsonify({'message': 'Logged out'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)