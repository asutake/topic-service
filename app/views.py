from app.application import app


@app.route('/')
def hello():
    return "Hello World!"
