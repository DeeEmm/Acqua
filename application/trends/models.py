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

from application.database import db
from datetime import datetime


# Trends - id | type | description | unit
class Trends(db.Model):
    __tablename__ = 'trends'
    id = db.Column(db.Integer, unique=True, primary_key=True, )
    description = db.Column(db.String(80))
    unit_of_measure = db.Column(db.Integer)
    trend_type = db.Column(db.Integer)
    
    def __repr__(self):
        return "<Trends: {}>".format(self.description)


# Trend_data - id | trend_id | datetime | value
class Trend_Data(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    trend_id = db.Column(db.Integer, unique=True, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    value = db.Column(db.String(80), unique=True, nullable=False)
    def __repr__(self):
        return "<Trend_Data: {}>".format(self.value)


db.create_all()