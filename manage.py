#!/usr/bin/env python
from flask_script import Manager, Shell, Server
from blog import app

manager = Manager(app)

@manager.command
def runserver():
    app.run(host='0.0.0.0')
manager.add_command("shell", Shell())

@manager.command
def createdb():
    from blog.models import db, User
    db.create_all()
    user = User('admin', 'admin@example.com',  'admin_pw1')
    db.session.add(user)
    db.session.commit()

manager.run()
