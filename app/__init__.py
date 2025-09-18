from flask import g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.exceptions import JWTExtendedException

class MockUser:
    def __init__(self, is_authenticated):
        self.is_authenticated = is_authenticated

def create_app():
    app = Flask(__name__)
    # ... остальной код создания приложения ...

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

    return app