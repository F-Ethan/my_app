from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class Users(db.Model):
	__tablename__='users'
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String, nullable=False)
	lsat_name = db.Column(db.String, nullable=False)
	password = db.Column(db.String, nullable=False)
	email = db.Column(db.string, nullable=False)
	time_created = db.Column(DateTime(timezone=True), server_default=func.now())
	time_updated = db.Column(DateTime(timezone=True), onupdate=func.now())

class transactions(db.Model):
	__tablename__=''