from datetime import timedelta
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY') or 'Maggie1234'
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    BASIC_AUTH_USERNAME = os.getenv("BASIC_AUTH_USERNAME") or 'admin'
    BASIC_AUTH_PASSWORD = os.getenv("BASIC_AUTH_PASSWORD") or '123456'
    ADMINS = ['no-reply@tallie.com']
    CLIENT_URL = os.getenv('CLIENT_URL') or 'http://127.0.0.1:5000'

    # ? For sqlite
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # ? For postgreSQL
    uri = os.getenv("DATABASE_URL")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = uri or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:123456@localhost/Vivilio'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']
    IMAGE_FOLDER_DIR = os.environ.get('IMAGE_FOLDER_DIR') or f'{basedir}\\app\\static\\images'

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or 'Maggie1234'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=300)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=300)