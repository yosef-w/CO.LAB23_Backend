from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from secrets import token_hex
from sqlalchemy.dialects.postgresql import ARRAY

db = SQLAlchemy()


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(100), nullable=True)
    apitoken = db.Column(db.String, unique=True)
    # username = db.Column(db.String(75), nullable=False, unique=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(75), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=True)
    prev_role = db.Column(db.String(100))
    prev_exp = db.Column(db.String(100))
    mentor = db.Column(db.Boolean, default=False)
    prod_role = db.Column(db.String(100))
    prod_exp = db.Column(db.String(100))
    adjectives = db.Column(ARRAY(db.String()))
    about = db.Column(db.String(500))
    interests = db.Column(ARRAY(db.String()))
    location = db.Column(db.String(100))
    timezone = db.Column(db.String(100))
    hours_wk = db.Column(db.String(100))
    availability = db.Column(ARRAY(db.String()))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    design_skills = db.Column(ARRAY(db.String()))
    developer_skills = db.Column(ARRAY(db.String()))
    management_skills = db.Column(ARRAY(db.String()))
    wanted_skills = db.Column(ARRAY(db.String()))
    linkedin = db.Column(db.String(100))
    github = db.Column(db.String(100))
    project = db.relationship("Projects")

    def __init__(self, first_name, last_name, email, password):
        super().__init__()
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
            "date_created": self.date_created,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "prev_role": self.prev_role,
            "prev_exp": self.prev_exp,
            "mentor": self.mentor,
            "prod_role": self.prod_role,
            "prod_exp": self.prod_exp,
            "adjectives": self.adjectives,
            "about": self.about,
            "interests": self.interests,
            "location": self.location,
            "timezone": self.timezone,
            "hours_wk": self.hours_wk,
            "availability": self.availability,
            "design_skills": self.design_skills,
            "developer_skills": self.developer_skills,
            "management_skills": self.management_skills,
            "wanted_skills": self.wanted_skills
        }

    # def __repr__(self):
    #     return f"<User {self.id}|{self.first_name}>"


class Projects(db.Model):

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(25), nullable=False)
    duration = db.Column(db.String(50))
    industries = db.Column(ARRAY(db.String()))
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    admin_timezone = db.Column(db.String(50))
    description = db.Column(db.String(500))
    hours_wk = db.Column(db.String(100))
    looking_for = db.Column(db.String(500))
    complete = db.Column(db.Boolean, unique=False, default=False)
    team_size = db.Column(db.Integer)
    need_pm = db.Column(db.Boolean, unique=False, default=True)
    need_designer = db.Column(db.Boolean, unique=False, default=True)
    need_dev = db.Column(db.Boolean, unique=False, default=True)

    def __init__(self, admin_id, name):
        super().__init__()
        self.admin_id = admin_id
        self.name = name

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

class ToDos():
    pass