from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.exceptions import JWTExtendedException
import os

# Создаем экземпляры расширений
db = SQLAlchemy()
jwt = JWTManager()

class MockUser:
    def __init__(self, is_authenticated):
        self.is_authenticated = is_authenticated

def create_app():
    app = Flask(__name__)
    
    # Определяем окружение
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object('app.config.ProductionConfig')
    else:
        app.config.from_object('app.config.DevelopmentConfig')
    
    # Инициализируем расширения
    db.init_app(app)
    jwt.init_app(app)
    
    # Добавляем контекстные процессоры
    @app.before_request
    def load_user():
        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
            g.user_authenticated = user_id is not None
        except JWTExtendedException:
            g.user_authenticated = False

    @app.context_processor
    def inject_user():
        return dict(current_user=MockUser(g.get('user_authenticated', False)))
    
    # Регистрируем blueprint'ы
    from app.auth import auth_bp
    from app.routes import main_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    
    # Создаем таблицы в базе данных
    with app.app_context():
        db.create_all()
        print("Database tables created")
    
    return app