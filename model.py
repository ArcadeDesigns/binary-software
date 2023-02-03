import os
from flask import Flask
from datetime import date
from datetime import datetime
from flask_login import UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

#create a flask instance
app = Flask(__name__)
#Add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fxglobal.db'

#initializing the database
db = SQLAlchemy(app)
migrate = Migrate(app,db)

class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False, unique=True)
	name = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(200), nullable=False, unique=True)
	date_added = db.Column(db.DateTime, default=datetime.utcnow)
	#Do Some Password Stuff
	password = db.Column(db.String(128))

class Links(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	youtube = db.Column(db.String(400), nullable=False)
	youtubeLabel = db.Column(db.String(200), nullable=False)