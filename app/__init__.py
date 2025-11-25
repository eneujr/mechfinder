from flask import Flask
from config import Config
from app.models import db, User
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.products import products_bp
    from app.routes.api import api_bp

    from app.routes.cart import cart_bp
    from app.routes.stores import stores_bp
    from app.routes.image_search import image_search_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(stores_bp)
    app.register_blueprint(image_search_bp)

    with app.app_context():
        db.create_all()
        # Optional: Add seed data here if empty

    return app
