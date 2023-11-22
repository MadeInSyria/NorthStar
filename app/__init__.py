from flask import Flask
from flask_bootstrap import Bootstrap5
from config import Config
from .extensions import db

# init SQLAlchemy so we can use it later in our models

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    Bootstrap5(app)

    db.init_app(app)

    # blueprint for auth routes in our app
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app