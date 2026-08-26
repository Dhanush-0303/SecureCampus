import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_login import LoginManager  # Added import
from app.config import config

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
login_manager = LoginManager()       # Created instance

def setup_logging(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')
        
    file_handler = RotatingFileHandler(
        'logs/securecampus.log', 
        maxBytes=10485760, 
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s [%(pathname)s:%(lineno)d]: %(message)s'
    ))
    file_handler.setLevel(getattr(logging, app.config.get('LOG_LEVEL', 'INFO')))
    
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('SecureCampus initialization started...')

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Extension Init
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    # Initialize LoginManager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    setup_logging(app)
    register_error_handlers(app)

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.api import api_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/')
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    app.logger.info('SecureCampus Startup Complete.')
    with app.app_context():
    db.create_all()
    return app