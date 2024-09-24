from os import environ


class Config(object):
    """Base configuration."""

    DB_HOST = "bd_name"
    DB_USER = "db_user"
    DB_PASS = "db_pass"
    DB_NAME = "db_name"
    SECRET_KEY = "secret"
    

    @staticmethod
    def configure(app):
        # Implement this method to do further configuration on your app.
        pass


class ProductionConfig(Config):
    """Production configuration."""
    
    ENV = "production"
    DEBUG = environ.get("DEBUG", False)
    DB_HOST = environ.get("DB_HOST", "https://sql.proyecto2021.linti.unlp.edu.ar/")
    DB_USER = environ.get("DB_USER", "grupo13")
    DB_PASS = environ.get("DB_PASS", "ZWI1MGIxNDVmZWI0")
    DB_NAME = environ.get("DB_NAME", "grupo13")
    GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID", "429358953753-1hpnm45ioc7le8kfihuu2nud259jj49g.apps.googleusercontent.com")
    GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET", "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")
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )


class DevelopmentConfig(Config):
    """Development configuration."""

    GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID", "429358953753-1hpnm45ioc7le8kfihuu2nud259jj49g.apps.googleusercontent.com")
    GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET", "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")
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )

    ENV = "development"
    DEBUG = environ.get("DEBUG", True)
    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_USER = environ.get("DB_USER", "root")
    DB_PASS = environ.get("DB_PASS", "root")
    DB_NAME = environ.get("DB_NAME","grupo13")

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_USER = environ.get("DB_USER", "MY_DB_USER")
    DB_PASS = environ.get("DB_PASS", "MY_DB_PASS")
    DB_NAME = environ.get("DB_NAME", "MY_DB_NAME")

    GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID", "429358953753-1hpnm45ioc7le8kfihuu2nud259jj49g.apps.googleusercontent.com")
    GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET", "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")
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )

config = dict(
    development=DevelopmentConfig, test=TestingConfig, production=ProductionConfig
)

## More information
# https://flask.palletsprojects.com/en/2.0.x/config/
