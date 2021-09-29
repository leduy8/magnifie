from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from config import Config

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
jwt = JWTManager()
ma = Marshmallow()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.administrator import init_admin
    init_admin(app)

    Path(f"{app.config['IMAGE_FOLDER_DIR']}").mkdir(parents=True, exist_ok=True)

    return app


from app import models, email, utils