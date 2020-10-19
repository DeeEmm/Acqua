MAJOR_VERSION = "1"
MINOR_VERSION = "0"
BUILD_NUMBER = "20102001"
RELEASE = "V.1.0-ALPHA"
VERSION = MAJOR_VERSION + '.' + MINOR_VERSION + '.' + BUILD_NUMBER
TESTING = True
DEBUG = True
FLASK_ENV = 'development'
# FLASK_APP = 'application.__init__.py'
# SERVER_NAME = 'acqua'
# SECRET_KEY = 'GDtfDCFYjD'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:////home/acqua/acqua.db'
# SQLALCHEMY_ECHO: # Prints db-related actions to console for debugging.
# SQLALCHEMY_ENGINE_OPTIONS: