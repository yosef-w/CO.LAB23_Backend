from app import app


@app.route('/')
def hello_world():
    return 'This is an API for the TeamUp app.'