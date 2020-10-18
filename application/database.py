from flask.ext.sqlalchemy import SQLAlchemy
from flask import current_app as app

# app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/acqua.db'
db = SQLAlchemy(app)
