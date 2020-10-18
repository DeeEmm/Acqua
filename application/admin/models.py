# Tables
# -----------------------
# admin - (configuration settings)
# trends - id | type | description | unit
# trend_data - id | trend_id | datetime | value
# nodes - id | type | description | unit
# node_setting - id | node_id | description | value
# cron_data - id | description | cron | action_type | action_value

# control_conditions
# id | operand1 | operand1_type | operand2 | operand2_type | operator |
# action_type | action_value

# control_actions - id | sequence | action_type | action | log
# event_log - id | type | datetime | value

# NOTE: Control Conditions
# Operand types = nodes / GPIO / other control conds / datetime / static values
# Operators = GT | LT | SGT | SLT | EQT
# Where >= is  "greater than" (GT) and > is "strictly greater than" (SGT).

# Control condition  / CRON
# Action types can be:
# control_action | boolean operator (AND / OR / NOT / NAND / XOR / XNOR)
# Action value is either control_action.sequence # | control_condition.id

# Control Actions
# Action_types:
# set / reset output | pulse output | send node API commands | send an email |
# create trend data entry | create a log entry | change an admin setting!?! |
# perform an admin function | run a script | run a shell command

import sqlite3
import os

from flask import Flask
from flask import render_template
from flask import request

# from datetime import datetime
# from click import command, echo
# from flask_sqlalchemy import SQLAlchemy
# from flask.cli import with_appcontext

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "acqua.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)


# Trends - id | type | description | unit
class trends(db.Model):
    id = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    type = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    description = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    value = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    def __repr__(self):
        return "<ID: {}>".format(self.id)
        return "<Type: {}>".format(self.type)
        return "<Description: {}>".format(self.description)
        return "<Value: {}>".format(self.value)


# Trend_data - id | trend_id | datetime | value
class trend_data(db.Model):
    id = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    trend_id = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    datetime = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    value = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    def __repr__(self):
        return "<ID: {}>".format(self.id)
        return "<Trend ID: {}>".format(self.trend_id)
        return "<DateTime: {}>".format(self.datetime)
        return "<Value: {}>".format(self.value)
