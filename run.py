from app import create_app, db

app = create_app()

# Всегда создаем таблицы при запуске приложения
with app.app_context():
    db.create_all()
    print("Database tables created")

if __name__ == '__main__':
    app.run(debug=False)