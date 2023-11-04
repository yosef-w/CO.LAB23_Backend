from . import api
from ..models import User, Projects, ToDo, Resources, Meetings, Links, Inspiration, Notifications
from flask import request
from .apiauthhelper import token_auth


@api.post('/createproject')
@token_auth.login_required
def createProject():
    data = request.json

    admin_id = data['admin_id']
    project_name = data['project_name']
    description = data['description']
    duration = data['duration']
    industries = data['industries']
    looking_for = data['looking_for']
    team = data['team_needed']

    user = User.query.get(admin_id)
    if user.current_project_id != None:
        return {
            'status': 'not ok',
            'message': "It looks like you're already involved in a project. Leave or complete that project before starting a new one!"
        }

    project = Projects.query.filter_by(name = project_name).first()
    if project:
        return {
            'status': 'not ok',
            'message': 'That project already exists.'
        }, 400
    project = Projects(admin_id=admin_id, name=project_name, description=description, duration=duration, industries=industries, looking_for=looking_for)

    # Adresses what roles the project needs. Default values in db are True
    if team['productManager'] == False:
        project.need_pm = False
    if team['productDesigner'] == False:
        project.need_designer = False
    if team['developer1'] == False and team['developer2'] == False:
        project.need_dev = False

    project.saveToDB()
    #Check to see if the project saved to the database successfully
    projectsaved = Projects.query.filter_by(name=project_name).first()
    if projectsaved:
        ## Associate the suer with the project
        user.current_project_id = projectsaved.id
        user.is_admin = True
        user.saveToDB()

        # Pre-poplulate some links for 'em!
        initial_links = ["Design File", "Repository", "Project Management", "Project Files", "Communication", "Meeting"]

        for title in initial_links:
            new_link = Links(project_id= projectsaved.id, title=title, content="Click to Enter")
            new_link.saveToDB()

        # Pre-populate sample 'Helpful Resource' and 'Inspiration' links
        resources = ["Resource 1", "Resource 2", "Resource 3", "Resource 4"]
        for resource in resources:
            new_resource = Resources(project_id = projectsaved.id, title=resource, content="Click to Enter")
            new_resource.saveToDB()

        inspirations = ["Inspiration 1", "Inspiration 2", "Inspiration 3", "Inspiration 4"]
        for inspiration in inspirations:
            new_inspo = Inspiration(project_id = projectsaved.id, title = inspiration, content="Click to Enter")
            new_inspo.saveToDB()

        # Pre-populate some tasks
        task1 = ToDo(project_id = projectsaved.id, title = "Monitor ‘Your Team' tab for newly joined team members.")
        task1.notes = "Contact members in the 'Your Team' tab."
        task1.saveToDB()

        task2 = ToDo(project_id = projectsaved.id, title = "Schedule first team meeting.")
        task2.saveToDB()

        return {
            'status': 'ok',
            'message': 'Project successfully created!',
            'project': projectsaved.to_dict(),
            'user': user.to_dict()
        }, 201
    else:
        return {
            'status': 'not ok',
            'message': 'Potential error in project creation or querying.'
        }, 400


@api.post('/addprojectuser')
@token_auth.login_required
def addProjectUser():
    data = request.json

    user_id = data['user_id']
    project_id = data['project_id']

    # Query for the user and project
    user = User.query.get(user_id)
    project = Projects.query.get(project_id)

    # Check if user or project does not exist
    if user is None or project is None:
        return {
            'status': 'not ok',
            'message': 'User or project not found.'
        }, 404

    # Check if the user is already part of another project
    if user.current_project_id != None:
        return {
            'status': 'not ok',
            'message': "It looks like you're already involved in another project! Leave or complete that project before joining another one."
        }, 401

    # Add user to the project
    user.current_project_id = project.id
    user.saveToDB()
    members = project.members
    for member in members:
        if member.id != user.id:
            notification = Notifications(user_id=member.id, content= f'{user.first_name} {user.last_name} has been added to your project!')
            notification.saveToDB()
        else:
            pass
    return {
        'status': 'ok',
        'message': f"You've been successfully to ${project.name}!",
        'project': project.to_dict(),
        #Sending back the user data as well to update current_project_id on the front end
        'user': user.to_dict()
    }, 200

@api.post('/removeprojectuser/<int:user_id>')
@token_auth.login_required
def removeProjectUser(user_id):

    user = User.query.get(user_id)

    if user:
        user.current_project_id = None
        if user.is_admin == True:
            user.is_admin = False
        user.saveToDB()
        return {
            'status': 'ok',
            'message': "You've been successfully removed from your current project."
        }, 200
        


@api.post('/addtask')
@token_auth.login_required
def addTask():
    data = request.json

    project_id = data['project_id']
    title = data['title']
    notes = data['notes']
    duedate = data['duedate']

    task = ToDo(project_id=project_id, title=title)
    task.notes = notes
    task.duedate = duedate

    try:
        task.saveToDB()
        return {
            'status': 'ok',
            'message': 'Task created!'
        }, 201
    except:
        return{
            'status': 'not ok',
            'message': 'Task not created.'
        }
    
@api.post('/deletetask/<int:task_id>')
@token_auth.login_required
def deleteTask(task_id):
    task = ToDo.query.get(task_id)
    project_id = task.project_id
    
    if task:
        task.deleteFromDB()
        tasks = ToDo.query.filter_by(project_id=project_id).all()
        return {
            'status': 'ok',
            'message': 'Task successfully deleted!',
            'tasks': [task.to_dict() for task in tasks]
        }
    else:
        return {
            'status': 'not ok',
            'message': "That task doesn't exist. It may have already been deleted."
        }
    
@api.post('/updatecompletedtask/<int:todo_id>')
@token_auth.login_required
def updateTask(todo_id):
    todo = ToDo.query.get(todo_id)
    project_id = todo.project_id
    project_todos = ToDo.query.filter_by(project_id=project_id).all()

    if todo:
        todo.completed = True
        todo.saveToDB()

        def sortItem(item):
            return item.id
    
        # Sort tasks so the most recent is first
        project_todos.sort(key=sortItem, reverse=True)

        return {
            'status': 'ok',
            'message': 'Task successfully marked as complete!',
            'tasks': [task.to_dict() for task in project_todos]
        }
    else:
        return {
            'status': 'not ok',
            'message': "Task not found. Refresh the page and try again."
        }
    
@api.post('/undotask/<int:task_id>')
@token_auth.login_required
def undoTask(task_id):
    task = ToDo.query.get(task_id)

    if task:
        task.completed = False
        task.saveToDB()

        project_id = task.project_id
        project_todos = ToDo.query.filter_by(project_id=project_id).all()

        def sortItem(item):
            return item.id
    
        # Sort tasks so the most recent is first
        project_todos.sort(key=sortItem, reverse=True)

        return {
            'status': 'ok',
            'message': 'Task successfully marked as incomplete!',
            'tasks': [task.to_dict() for task in project_todos]
        }
    else:
        return {
            'status': 'not ok',
            'message': "Task not found. Refresh the page and try again."
        }
        
@api.get('/gettasks/<int:project_id>')
@token_auth.login_required
def getTasks(project_id):

    tasks = ToDo.query.filter_by(project_id=project_id).all()
    meetings = Meetings.query.filter_by(project_id=project_id).all()

    def sortItem(item):
        return item.id
    
    # Sort meetings and tasks so the most recent is first
    tasks.sort(key=sortItem, reverse=True)
    meetings.sort(key=sortItem, reverse=True)

    if tasks or meetings:
        return {
            'status': 'ok',
            'tasks': [task.to_dict() for task in tasks],
            'meetings': [meeting.to_dict() for meeting in meetings]
        }
    else:
        return {
            'status': 'ok',
            'message': 'The project has no tasks'
        }


# Gets team info for a project to display on the dashboard Your Team tab
@api.get('/getteam/<int:project_id>')
@token_auth.login_required
def getTeam(project_id):
    project = Projects.query.get(project_id)

    if project:
        members = project.members
        return {
            'status': 'ok',
            'members': [member.to_dict() for member in members],
            'team_size': len(members)
        }
    
@api.post('/createresource')
@token_auth.login_required
def createResource():
    data = request.json

    project_id = data['project_id']
    type = data['type']
    title = data['title']
    content = data['content']

    if type == 'Project Link':
        try:
            link = Links(project_id=project_id, title=title, content=content)
            link.saveToDB()
            return {
                'status': 'ok',
                'message': 'New Project Link successfully saved!'
            }
        except:
            return {
                'status': 'not ok',
                'message': "New Project Link couldn't be saved!"
            }
        
    elif type == 'Helpful Resource':
        try:
            link = Resources(project_id=project_id, title=title, content=content)
            link.saveToDB()
            return {
                'status': 'ok',
                'message': 'New Helpful Resource successfully saved!'
            }
        except:
            return {
                'status': 'not ok',
                'message': "New Helpful Resource couldn't be saved!"
            }
        
    elif type == 'Inspiration':
        try:
            link = Inspiration(project_id=project_id, title=title, content=content)
            link.saveToDB()
            return {
                'status': 'ok',
                'message': 'New Inspiration successfully saved!'
            }
        except:
            return {
                'status': 'not ok',
                'message': "New Inspiration couldn't be saved!"
            }
    
@api.get('/getresources/<int:project_id>')
@token_auth.login_required
def getResources(project_id):
    resources = Resources.query.filter_by(project_id=project_id).all()
    links = Links.query.filter_by(project_id=project_id).all()
    inspiration = Inspiration.query.filter_by(project_id=project_id).all()

    def sortItem(item):
        return item.id
    
    resources.sort(key=sortItem)
    links.sort(key=sortItem)
    inspiration.sort(key=sortItem)

    return {
        'status': 'ok',
        'resources': [resource.to_dict() for resource in resources],
        'links': [link.to_dict() for link in links],
        'inspiration': [inspo.to_dict() for inspo in inspiration]
    }

@api.post('/updateresources')
@token_auth.login_required
def updateResources():
    data = request.json

    type = data['type']
    resource_id = data['resource_id']
    title = data['title']
    content = data['content']

    if type == 'links':
        link = Links.query.get(resource_id)
        if link:
            link.title = title
            link.content = content
            link.saveToDB()

            return {
                'status': 'ok',
                'message': 'Project Links have been updated!'
            }, 200
        else:
            return {
                'status': 'not ok',
                'message': "That Project Link couldn't be found!"
            }, 404
    
    elif type == 'resources':
        link = Resources.query.get(resource_id)
        if link:
            link.title = title
            link.content = content
            link.saveToDB()

            return {
                'status': 'ok',
                'message': 'Helpful Resources have been updated!'
            }, 200
        else:
            return {
                'status': 'not ok',
                'message': "That Resource couldn't be found!"
            }, 404

    elif type == 'inspiration':
        link = Inspiration.query.get(resource_id)
        if link:
            link.title = title
            link.content = content
            link.saveToDB()

            return {
                'status': 'ok',
                'message': 'Inspirations have been updated!'
            }, 200
        else:
            return {
                'status': 'not ok',
                'message': "That Inspiration couldn't be found!"
            }, 404
        
@api.post('/deleteresource')
@token_auth.login_required
def deleteResource():
    data = request.json

    type = data['type']
    resource_id = data['resource_id']

    if type == 'links':
        link = Links.query.get(resource_id)
        if link:
            link.deleteFromDB()

            return {
                'status': 'ok',
                'message': 'Project Link successfully deleted!'
            }, 200
        else:
            return {
                'status': 'not ok',
                'message': "That Project Link couldn't be found!"
            }, 404
    
    elif type == 'resources':
        link = Resources.query.get(resource_id)
        if link:
            link.deleteFromDB()

            return {
                'status': 'ok',
                'message': 'Helpful Resource successfully deleted!'
            }, 200
        else:
            return {
                'status': 'not ok',
                'message': "That Resource couldn't be found!"
            }, 404

    elif type == 'inspiration':
        link = Inspiration.query.get(resource_id)
        if link:
            link.deleteFromDB()

            return {
                'status': 'ok',
                'message': 'Inspiration successfully deleted!'
            }, 200
        else:
            return {
                'status': 'not ok',
                'message': "That Inspiration couldn't be found!"
            }, 404

@api.post('/addmeeting')
@token_auth.login_required
def addMeeting():
    data = request.json

    project_id = data['project_id']
    title = data['title']
    date = data['date']  
    notes = data['notes']  

    try:
        meeting = Meetings(project_id, title, date, notes)
        meeting.saveToDB()
        return {
            'status': 'ok',
            'message': 'Meeting successfully saved!'
        }
    except:
        return {
            'status': 'not ok',
            'message': 'Meeting might not have been saved.'
        }
    
@api.post('/deletemeeting/<int:meeting_id>')
@token_auth.login_required
def deleteMeeting(meeting_id):
    meeting = Meetings.query.get(meeting_id)
    project_id = meeting.project_id
    
    if meeting:
        meeting.deleteFromDB()
        meetings = Meetings.query.filter_by(project_id=project_id).all()
        return {
            'status': 'ok',
            'message': 'Meeting successfully deleted!',
            'meetings': [meeting.to_dict() for meeting in meetings]
        }
    else:
        return {
            'status': 'not ok',
            'message': "That meeting doesn't exist. It may have already been deleted."
        }

@api.get('/getteamsbrowser')
@token_auth.login_required
def teamsBrowser():
    projects = Projects.query.all()
    users = User.query.all()

    return {
        'status': 'ok',
        'projects': [project.to_dict() for project in projects],
        'users': [user.to_dict() for user in users],
        'number_of_projects': len(projects),
        'number_of_users': len(users)
    }

@api.get('/getuser/<int:user_id>')
# @token_auth.login_required
def getUser(user_id):
    user = User.query.get(user_id)


    if user.current_project_id:
        admin_name = f'{user.current_project.admin.first_name} {user.current_project.admin.last_name}'
        return {
            'status': 'ok',
            'user': user.to_dict(),
            'project': user.current_project.to_dict()
        }
    elif user:
        return {
            'status': 'ok',
            'user': user.to_dict(),
        }
    else:
        return {
            'status': 'not ok',
            'message': 'User not found.'
        }
    
@api.get('/getproject/<int:project_id>')
# @token_auth.login_required
def getProject(project_id):
    project = Projects.query.get(project_id)

    if project:
        return {
            'status': 'ok',
            'project': project.to_dict(),
            'admin': project.admin.to_dict()
        }
    else:
        return {
            'status': 'not ok',
            'message': 'Project not found.'
        }