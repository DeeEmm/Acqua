from flask.ext.sqlalchemy import SQLAlchemy
from flask import current_app as app

app.config.from_envvar('APP_CONFIG_FILE')
db = SQLAlchemy(app)
