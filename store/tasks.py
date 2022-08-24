from celery import Celery

# Celery('module', broker)
app = Celery('tasks', broker="redis://localhost")

@app.task
def add(x,y):
    return x+y
