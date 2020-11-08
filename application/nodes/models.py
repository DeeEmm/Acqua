from application.database import db
from sqlalchemy.sql import func

# Nodes
class Nodes(db.Model):
	__tablename__ = 'nodes'
	id = db.Column(db.Integer, unique=True, primary_key=True, )
	description = db.Column(db.String(80))
	i2c_address = db.Column(db.Integer)

	def __repr__(self):
		return "<Nodes: {}>".format(self.description)

db.create_all()
