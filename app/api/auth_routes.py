from . import api
from ..models import User
from flask import request

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

#Will be called at the end of onboarding to finalize creation of a new user.
@api.post('/signup')
def signUpAPI():
    data = request.json

    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    password = data['password']

    #Checks if user already exists
    user = User.query.filter_by(email = email).first()
    if user:
        return {
            'status': 'not ok',
            'message': 'That email already exists, please choose a different one.'
        }, 400
    
    user = User(first_name, last_name, email, password)
    user.saveToDB()
    return {
        'status': 'ok',
        'message': 'Account successfully created!'
    }, 201