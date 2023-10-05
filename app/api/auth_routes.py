from . import api
from ..models import User
from flask import request

@api.post('/signup')
def signUpAPI():
    data = request.json

    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    password = data['password']

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