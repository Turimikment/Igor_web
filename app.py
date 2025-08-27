from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from config import Config
from models import db
from routes.auth import auth_bp
from routes.products import products_bp
from routes.favorites import favorites_bp
from auth import token_required
import atexit
from routes.cart import cart_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
swagger = Swagger(app)

# Регистрация blueprint'ов
app.register_blueprint(auth_bp)
app.register_blueprint(products_bp, url_prefix='/api')
app.register_blueprint(favorites_bp, url_prefix='/api')
app.register_blueprint(cart_bp, url_prefix='/api')
# === Инициализация БД ===
def init_database():
    with app.app_context():
        db.create_all()
        print("✅ Таблицы созданы")

        # Тестовый пользователь
        if not User.query.filter_by(username='admin').first():
            from werkzeug.security import generate_password_hash
            admin = User(
                username='admin',
                email='admin@example.com',
                password_hash=generate_password_hash('admin'),
                is_active=True
            )
            db.session.add(admin)
            db.session.commit()
            print("🆕 Пользователь 'admin' добавлен")

        # Тестовые товары
        if Product.query.count() == 0:
            products = [
                Product(name="Ноутбук", price=59990.00, description="Мощный ноутбук", image_url="https://via.placeholder.com/150?text=Notebook"),
                Product(name="Смартфон", price=29990.00, description="Флагманский смартфон", image_url="https://via.placeholder.com/150?text=Phone"),
                Product(name="Наушники", price=4990.00, description="С шумоподавлением", image_url="https://via.placeholder.com/150?text=Headphones"),
            ]
            db.session.bulk_save_objects(products)
            db.session.commit()
            print("🆕 Добавлено 3 товара")

init_database()
atexit.register(lambda: print("🛑 Приложение остановлено"))

# === Главные страницы ===
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    return render_template('products.html')

if __name__ == '__main__':
    app.run(debug=False)