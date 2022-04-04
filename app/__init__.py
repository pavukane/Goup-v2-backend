import os
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_session import Session
from config import Config

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()

bcrypt = Bcrypt()
server_session = Session()


def init_app():
    app = Flask(__name__)
    app.config.from_object(Config or os.environ['APP_SETTINGS'])
    # init
    cors.init_app(app, supports_credentials=True, origins=["http://localhost:3000"] )
    db.init_app(app)

    app.config["SESSION_SQLALCHEMY"] = db
    migrate.init_app(app, db)

    bcrypt.init_app(app)
    server_session.init_app(app)
    # import auth blueprints
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth') 
    # import main blueprints
    from app.main import main_bp
    app.register_blueprint(main_bp)

    return app


from app.models import User # put this in bottom if not migrating


