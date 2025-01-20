from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from website.config import Config
from flask_socketio import SocketIO
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()


def create_app():
    """ Creates and configures the Flask application. """
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    # Register blueprints
    from .routes.authentication import authentication
    from .routes.main_routes import main_routes_bp
    from .routes.user_routes import user_routes_bp
    from .routes.friendship_routes import friendship_routes_bp
    from .routes.conversation_routes import conversation_routes_bp
    from .routes.group_routes import group_routes_bp
    from .routes.message_routes import message_routes_bp
    from .routes.notification_routes import notification_routes_bp

    app.register_blueprint(main_routes_bp, url_prefix='/')
    app.register_blueprint(authentication, url_prefix='/')
    app.register_blueprint(user_routes_bp, url_prefix='/')
    app.register_blueprint(friendship_routes_bp, url_prefix='/')
    app.register_blueprint(conversation_routes_bp, url_prefix='/')
    app.register_blueprint(group_routes_bp, url_prefix='/')
    app.register_blueprint(message_routes_bp, url_prefix='/')
    app.register_blueprint(notification_routes_bp, url_prefix='/')

    # Import models after app is fully initialized
    from website.models.user import User
    from website.models.message import Message
    from website.models.notification import Notification
    from website.models.friendship import Friendship
    from website.models.group import Group
    from website import socket_events

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(str(id))

    return app

