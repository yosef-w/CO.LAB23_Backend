from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from secrets import token_hex
from sqlalchemy.dialects.postgresql import ARRAY

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "user"

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
    other_skills = db.Column(ARRAY(db.String()))
    linkedin = db.Column(db.String(100))
    github = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, unique=False, default=False)
    current_project_id = db.Column(db.Integer, db.ForeignKey('projects.id', use_alter=True, name='fk_user_projects'), nullable=True)  # Foreign key to the project
    current_project = db.relationship("Projects", foreign_keys=[current_project_id], back_populates="members", lazy='joined')
    notifications = db.relationship('Notifications', backref='user')

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
            "other_skills": self.other_skills,
            "wanted_skills": self.wanted_skills,
            "is_admin": self.is_admin,
            "current_project_id": self.current_project_id
        }

    # def __repr__(self):
    #     return f"<User {self.id}|{self.first_name}>"


class Projects(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(25), nullable=False, unique=True)
    duration = db.Column(db.String(50))
    industries = db.Column(ARRAY(db.String()))
    admin_timezone = db.Column(db.String(50))
    description = db.Column(db.String(1000), nullable=False)
    hours_wk = db.Column(db.String(100))
    looking_for = db.Column(db.String(500))
    complete = db.Column(db.Boolean, unique=False, default=False)
    team_size = db.Column(db.Integer)
    need_pm = db.Column(db.Boolean, unique=False, default=True)
    need_designer = db.Column(db.Boolean, unique=False, default=True)
    need_dev = db.Column(db.Boolean, unique=False, default=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    pms_wanted = db.Column(db.Integer)
    devs_wanted = db.Column(db.Integer)
    designers_wanted = db.Column(db.Integer)
    admin_id = db.Column(db.Integer, db.ForeignKey("user.id", use_alter=True, name='fk_projects_user'), nullable=False)
    admin = db.relationship('User', foreign_keys=[admin_id], backref="created_projects", lazy='joined')
    members = db.relationship('User', foreign_keys=[User.current_project_id], back_populates="current_project", lazy='joined')
    todos = db.relationship('ToDo', back_populates="project", cascade='all, delete, delete-orphan', lazy='joined')  # One-to-many with Todo
    resources = db.relationship('Resources', cascade="all, delete, delete-orphan")
    meetings = db.relationship('Meetings', cascade="all, delete, delete-orphan")
    links = db.relationship('Links', cascade="all, delete, delete-orphan")
    inspiration = db.relationship('Inspiration', cascade="all, delete, delete-orphan")


    def __init__(self, admin_id, name, description, duration, industries, looking_for):
        self.admin_id = admin_id
        self.name = name
        self.description = description
        self.duration = duration
        self.industries = industries
        self.looking_for = looking_for

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "duration": self.duration,
            "industries": self.industries,
            "admin_timezone": self.admin.timezone,
            "description": self.description,
            "hours_wk": self.hours_wk,
            "looking_for": self.looking_for,
            "complete": self.complete,
            "team_size": len(self.members),
            "need_pm": self.need_pm,
            "need_designer": self.need_designer,
            "need_dev": self.need_dev,
            "date_created": self.date_created,
            "admin_id": self.admin_id,
            "admin_name": f'{self.admin.first_name} {self.admin.last_name}'
        }


# Association table for User<->Todo many-to-many relationship
todos_users = db.Table('todos_users',
    db.Column('user_id', db.Integer,db.ForeignKey('user.id')),
    db.Column('todo_id', db.Integer,db.ForeignKey('todo.id')),
    db.metadata
    )


class ToDo(db.Model):
    __tablename__ = "todo"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    completed = db.Column(db.Boolean, default=False)
    title = db.Column(db.String(250), nullable=False)
    notes = db.Column(db.String(500))
    duedate = db.Column(db.String(100))
    # This creates a one-to-many relationship with Projects.
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    project = db.relationship('Projects', foreign_keys=[project_id], back_populates='todos', lazy='joined')
    users = db.relationship('User', secondary=todos_users, back_populates='todos', lazy='joined')  # Many-to-many with User

    def __init__(self, project_id, title):
        self.project_id = project_id
        self.title = title

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "completed": self.completed,
            "title": self.title,
            "notes": self.notes,
            "project_id": self.project_id,
            "duedate": self.duedate
        }


class Resources(db.Model):
    __tablename__ = "resources"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    project = db.relationship("Projects", back_populates="resources")
    title = db.Column(db.String(50))
    content = db.Column(db.String(500))

    def __init__(self, project_id, title, content):
        self.project_id = project_id
        self.title = title
        self.content = content

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "title": self.title,
            "content": self.content
        }


class Meetings(db.Model):
    __tablename__ = "meetings"
    
    id = db.Column(db.Integer, primary_key=True, unique=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    project = db.relationship("Projects", back_populates="meetings")
    title = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(100))
    notes = db.Column(db.String(500))

    def __init__(self, project_id, title, date, notes):
        self.project_id = project_id
        self.title = title
        self.date = date
        self.notes = notes

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "title": self.title,
            "date": self.date,
            "notes": self.notes
        }
    

class Links(db.Model):
    __tablename__ = "links"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    project = db.relationship("Projects", back_populates="links")
    title = db.Column(db.String(250), nullable=False)
    content = db.Column(db.String(500))

    def __init__(self, project_id, title, content):
        self.project_id = project_id
        self.title = title
        self.content = content

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "title": self.title,
            "content": self.content
        }
    
class Inspiration(db.Model):
    __tablename__ = "inspiration"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    project = db.relationship("Projects", back_populates="inspiration")
    title = db.Column(db.String(50))
    content = db.Column(db.String(500))

    def __init__(self, project_id, title, content):
        self.project_id = project_id
        self.title = title
        self.content = content

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "title": self.title,
            "content": self.content
        }
    
class Notifications(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(500))
    seen = db.Column(db.Boolean, unique=False, default=False)

    def __init__(self, user_id, content):
        self.user_id = user_id
        self.content = content

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "content": self.content
        }
    
    def notifyUsers(message):
        users = User.query.all()
        for user in users:
            notification = Notifications(user.id, message)
            notification.saveToDB()
    
# Association table for User<->Projects many-to-many relationship to track a user's past projects
user_projects_association = db.Table('user_projects_association',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id')),
    db.metadata
)


# After all model classes are defined, add the relationships that refer to later models.
User.todos = db.relationship('ToDo', secondary=todos_users, back_populates='users', lazy='joined')  # Many-to-many with Todo
User.past_projects = db.relationship('Projects', secondary=user_projects_association, lazy='dynamic', backref=db.backref('past_users', lazy='dynamic'))

