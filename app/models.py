from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from secrets import token_hex

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(50), nullable=True)
    apitoken = db.Column(db.String, unique=True)
    # username = db.Column(db.String(75), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(75), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=True)
    prev_role = db.Column(db.String(50))
    prev_exp = db.Column(db.String(50))
    mentor = db.Column(db.Boolean, default=False)
    prod_role = db.Column(db.String(50))
    prod_exp = db.Column(db.String(50))
    adjectives = db.Column(db.String(100))
    about = db.Column(db.String(500))
    interests = db.Column(db.String(200))
    location = db.Column(db.String(50))
    timezone = db.Column(db.String(50))
    hours_wk = db.Column(db.String(30))
    availability = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    design_skills = db.Column(db.String(200))
    developer_skills = db.Column(db.String(200))
    management_skills = db.Column(db.String(200))
    wanted_skills = db.Column(db.String(200))
    linkedin = db.Column(db.String(100))
    github = db.Column(db.String(100))

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)
        self.apitoken = token_hex(16)

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "apitoken": self.apitoken,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "prev_role": self.prev_role,
            "prev_exp": self.prev_exp,
            "mentor": self.prev_exp,
            "prod_role": self.prod_role,
            "prod_exp": self.prod_exp,
            "adjectives": self.adjectives,
            "about": self.about,
            "interests": self.interests,
            "location": self.location,
            "timezone": self.timezone,
            "hours_wk": self.hours_wk,
            "availability": self.availability,
            "date_created": self.date_created,
            "design_skills": self.design_skills,
            "developer_skills": self.developer_skills,
            "management_skills": self.management_skills,
            "wanted_skills": self.wanted_skills
        }

    # def __repr__(self):
    #     return f"<User {self.id}|{self.first_name}>"
