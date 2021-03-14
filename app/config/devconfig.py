from .baseconfig import BaseConfig


class DevConfig(BaseConfig):
    DEBUG = True
    SECRET_KEY = "developmentsecretkey"
    # SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/cardiopredict"
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:root@localhost:3306/cardiopredict"
