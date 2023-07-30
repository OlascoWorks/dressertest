from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import os
db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv(SECRET_KEY)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    env_config = os.getenv("PROD_APP_SETTINGS", "config.DevelopmentConfig")
    app.config.from_object(env_config)
    db.init_app(app)

    from .views import views
    from .auth import auth

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html', user=current_user)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Cloth
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
