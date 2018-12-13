import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ENVIROBASE_ADMIN = os.environ.get("ENVIROBASE_ADMIN")
    ENVIROBASE_POSTS_PER_PAGE = 20
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class Development(Config):
    """
    Development environment configuration
    """

    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL")

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class Production(Config):
    """
    Production environment configuration
    """

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    "development": Development,
    "production": Production,
    "default": Development,
}
