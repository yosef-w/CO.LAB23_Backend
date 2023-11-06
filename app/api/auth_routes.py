from . import api
from ..models import User, Projects, ToDo, Notifications
from flask import request
from werkzeug.security import check_password_hash
from .apiauthhelper import basic_auth_required, token_auth_required, basic_auth, token_auth

#Checks to see if a user already exists. Will be called after a user either clicks sign in with Google or uses the traditional sign up method with email/password before proceeding with account creation/onboarding.
@api.get('/checkuser/<email>')
def checkUser(email):
    # data = request.json
    # email = data['email']

    user = User.query.filter_by(email = email).first()
    if user:
        return {
            'status': 'not ok',
            'message': 'A user with that email already exists. Please choose a different email to use.'
        }, 400
    else:
        return {
            'status': 'ok',
            'message': 'The email entered is available. Proceed with onboarding process.'
        }, 200

#Will be called at the end of onboarding to finalize creation of a new user and save them to the database.
@api.post('/signup')
def signUpAPI():
    data = request.json

    first_name = data["personalForm"]['firstName']
    last_name = data["personalForm"]['lastName']
    email = data["personalForm"]['email']
    password = data["personalForm"]['password']

    prev_role = data["professionalBackground"]["previousRole"]
    # prev_exp = data["professionalBackground"]["yearsOfExperience"]
    mentor = data["professionalBackground"]["isMentor"]
    prod_role = data["professionalBackground"]["productRole"]
    prod_exp = data["professionalBackground"]["productExperience"]

    adjectives = data["aboutYouForm"]["adjectives"]
    about = data["aboutYouForm"]["description"]
    interests = data["aboutYouForm"]["fieldsOfInterest"]

    location = data["availabilityForm"]["location"]
    timezone = data["availabilityForm"]["timezone"]
    hours_wk = data["availabilityForm"]["hoursPerWeek"]
    availability = data["availabilityForm"]["availability"]

    design_skills = data["skillsTools"]["designSkills"]
    developer_skills = data["skillsTools"]["developerSkills"]
    management_skills = data["skillsTools"]["managementSkills"]
    wanted_skills = data["skillsTools"]["wantedSkills"]
    other_skills = data["skillsTools"]["otherSkills"]

    #Checks if user already exists, just in case!
    user = User.query.filter_by(email = email).first()
    if user:
        return {
            'status': 'not ok',
            'message': 'A user with that email already exists. Please choose a different email to use.'
        }, 400
    
    #Creates new User instance
    user = User(first_name, last_name, email, password)

    #Adds remaining User column data to new User from JSON data
    # google uid (user.uid) should be involved somehow
    user.prev_role = prev_role
    # user.prev_exp = prev_exp
    user.mentor = mentor
    user.prod_role = prod_role
    user.prod_exp = prod_exp

    user.adjectives = adjectives
    user.about = about
    user.interests = interests

    user.location = location
    user.timezone = timezone
    user.hours_wk = hours_wk
    user.availability = availability

    user.design_skills = design_skills
    user.developer_skills = developer_skills
    user.management_skills = management_skills
    user.other_skills = other_skills
    user.wanted_skills = wanted_skills

    # Finalize and save User creation to database
    user.saveToDB()

    #Check if creation was successful and the new user exists in database
    user_check = User.query.filter_by(email = email).first()
    if user_check:
        return {
            'status': 'ok',
            'message': 'Account successfully created!',
            'user': user.to_dict()
        }, 201
    else:
        return {
            'status': 'not ok',
            'message': 'Error creating User. Creation Unsuccessful.'
        }, 400
    
@api.post('/login')
@token_auth_required
def logInAPI(user):
    # user = basic_auth.current_user()
    user_project = Projects.query.filter_by(id=user.current_project_id).first()
    
    if user_project:

        def sortItem(item):
            return item.id
        
        resources = user_project.resources
        links = user_project.links
        inspiration = user_project.inspiration
    
        # Sort so the most recent is first
        resources.sort(key=sortItem)
        links.sort(key=sortItem)
        inspiration.sort(key=sortItem)

        notifications = Notifications.query.filter_by(user_id= user.id, seen = False).all()
        for notification in notifications:
            notification.seen = True
            notification.saveToDB()

        return {
                'status': 'ok',
                'message': 'Login successful!',
                'user': user.to_dict(),
                'project': user_project.to_dict(),
                'project_team': [member.to_dict() for member in user_project.members],
                'project_resources': [resource.to_dict() for resource in resources],
                'project_links': [link.to_dict() for link in links],
                'project_inspiration': [inspiration.to_dict() for inspiration in inspiration],
                'notifications': [notification.to_dict() for notification in notifications] if notifications else None
            }, 201
    else:
        return {
                'status': 'ok',
                'message': 'Login successful!',
                'user': user.to_dict()
            }, 201