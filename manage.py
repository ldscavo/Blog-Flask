#!/usr/bin/env python
from flask.ext.script import Manager, Shell, Server
from blog import app

manager = Manager(app)

@manager.command
def runserver():
    app.run(host='0.0.0.0')
manager.add_command("shell", Shell())

@manager.command
def createdb():
    from blog.models import db
    db.create_all()

manager.run()
