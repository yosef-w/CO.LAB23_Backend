from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from secrets import token_hex

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    apitoken = db.Column(db.String, unique = True)
    #username = db.Column(db.String(75), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(75), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    linkedin = db.Column(db.String(100))
    github = db.Column(db.String(100))
    #current profession role/title
    prof_title = db.Column(db.String(50))
    prof_exp = db.Column(db.String(50))
    prod_title = db.Column(db.String(50))
    prod_exp = db.Column(db.String(50))
    mentor = db.Column(db.Boolean, default=False)
    skills = db.Column(db.String(200))
    currently_learning = db.Column(db.String(200))
    interests = db.Column(db.String(200))
    adjectives = db.Column(db.String(100))
    about = db.Column(db.String(500))

    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash('password')

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.id}|{self.username}>"
