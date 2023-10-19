from . import api
from ..models import User, Projects
from flask import request
from .apiauthhelper import token_auth

@api.post('/creatproject')
@token_auth.login_required
def createProject():
    data = request.json
    admin_id = data['admin_id']
    project_name = data['project_name']

    project = Projects(admin_id = admin_id, name = project_name)

@api.post('/add-user-to-project')
@token_auth.login_required
def addUserToProject(user_id, project_id):

    # Query for the user and project
    user = User.query.get(user_id)
    project = Projects.query.get(project_id)

    # Check if user or project does not exist
    if user is None or project is None:
        return {
            'status': 'not ok',
            'message': 'User or project not found.'
            }, 400

    # Check if the user is already part of another project
    if user.current_project_id is not False:
        return {
            'status': 'not ok',
            'message': 'User is already part of a different project.'
            }, 400

    # Add user to the project
    user.current_project_id = project.id
    user.saveToDB()

    return {
        'status': 'ok',
        'message': 'User added to project successfully'
    }, 200
