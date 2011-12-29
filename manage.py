# -*- encoding: utf-8 -*-
"""
    :copyright: (c) 2011 by daisuke igarashi.
"""
import os
import sys
import shutil
import getpass

from flask.ext.script import Manager
from app.lib.mypassword import get_password_hash
from app.db import db_session, init_db, User, UserRole
from app import settings, app

manager = Manager(app)

@manager.command
def debug():
    app.run(debug=True, port=5000)

@manager.command
def init():
    try:
        if os.path.exists(settings.DATA_DIR_PATH):
            shutil.rmtree(settings.DATA_DIR_PATH)
        os.mkdir(settings.DATA_DIR_PATH)
        if os.path.exists(settings.DEMO_DIR_PATH):
            shutil.rmtree(settings.DEMO_DIR_PATH)
        os.mkdir(settings.DEMO_DIR_PATH)
        if os.path.exists(settings.THUMBNAIL_DIR_PATH):
            shutil.rmtree(settings.THUMBNAIL_DIR_PATH)
        os.mkdir(settings.THUMBNAIL_DIR_PATH)
    except:
        print sys.exc_info()
        
    try:
        if os.path.exists(settings.DB_PATH):
            os.remove(settings.DB_PATH)
        init_db()
    except:
        print sys.exc_info()

    try:
        role_admin = UserRole('admin', 'for administrators')
        db_session.add(role_admin)

        user_admin = User('admin', role=role_admin)
        db_session.add(user_admin)

        db_session.commit()
        db_session.remove()

    except:
        print sys.exc_info()

@manager.command
def adminpassword():
    admin_username = "admin"

    password = getpass.getpass()
    if len(password)<8:
        print "dame"
        return

    admin = User.query.get(1)

    if not admin:
        userrole = UserRole.query.get('admin')
        admin = User(admin_username, userrole)
        db_session.add(admin)
    
    admin.set_password(password)

    db_session.commit()
    db_session.remove()

    print "update successfully"

if __name__ == "__main__":
    manager.run()
