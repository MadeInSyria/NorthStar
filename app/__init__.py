from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config
from .extensions import db

# init SQLAlchemy so we can use it later in our models

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    Bootstrap5(app)

    db.init_app(app)
    migrate = Migrate(app, db)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from app.models.users import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for main pages
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for cabinets
    from app.cabinet import cabinet as cabinet_blueprint
    app.register_blueprint(cabinet_blueprint)
    
    # blueprint for drawers
    from app.drawer import drawer as drawer_blueprint
    app.register_blueprint(drawer_blueprint)
    
    return app