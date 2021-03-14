from .baseconfig import BaseConfig


class DevConfig(BaseConfig):
    DEBUG = True
    SECRET_KEY = "developmentsecretkey"
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"
