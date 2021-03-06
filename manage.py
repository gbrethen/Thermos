import os

from thermos import app
from thermos import db
from thermos.models import User
from flask_script import Manager, prompt_bool

manager = Manager(app)

@manager.command
def initdb():
    db.create_all()
    db.session.add(User(username="gbrethen", email="gbrethen@att.net"))
    db.session.commit()
    print('Initialized Database.')

@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data?"):
        db.drop_all()
        print('Dropped the database.')

if __name__ == '__main__':
    manager.run()
