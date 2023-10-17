from . import api
from ..models import User
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
    prev_exp = data["professionalBackground"]["yearsOfExperience"]
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
    user.prev_exp = prev_exp
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
    user.wanted_skills = wanted_skills

    # Finalize and save User creation to database
    user.saveToDB()

    #Check if creation was successful and the new user exists in database
    user_check = User.query.filter_by(email = email).first()
    if user_check:
        return {
            'status': 'ok',
            'message': 'Account successfully created!'
        }, 201
    else:
        return {
            'status': 'not ok',
            'message': 'Error creating User. Creation Unsuccessful.'
        }, 400
    
@api.post('/login')
@basic_auth.login_required
def logInAPI():
    user = basic_auth.current_user()

    return {
            'status': 'ok',
            'message': 'Login successful!',
            'data': user.to_dict()
        }, 201
