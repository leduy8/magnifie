import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY') or 'Maggie1234'
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    ADMINS = ['no-reply@tallie.com']

    # ? For sqlite
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(base_dir, 'app.db')
    # ? For postgreSQL
    # uri = os.getenv("DATABASE_URL")
    # if uri.startswith("postgres://"):
    #     uri = uri.replace("postgres://", "postgresql://", 1)
    # SQLALCHEMY_DATABASE_URI = uri or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:123456@localhost/Magnifie'
    SQLALCHEMY_TRACK_MODIFICATIONS = False