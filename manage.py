# -*- encoding: utf-8 -*-
"""
    :copyright: (c) 2011 by daisuke igarashi.
"""
import os
import sys
import shutil
import getpass
from pwd import getpwnam, getpwuid

from flask.ext.script import Manager
from app.lib.mypassword import get_password_hash
from app.db import db_session, init_db, User, UserRole
from app import settings, app

manager = Manager(app)

APACHE_USERNAME = "apache"
apache_uid = getpwnam(APACHE_USERNAME)[2]
apache_gid = getpwnam(APACHE_USERNAME)[3]

def remakedir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    if getpwuid(os.getuid())[0] == 'root':
        os.chown(path, apache_uid, apache_gid)

@manager.command
def init():
    """initialize database and directories"""
    try:
        remakedir(settings.DATA_DIR_PATH)
        remakedir(settings.DEMO_DIR_PATH)
        remakedir(settings.THUMBNAIL_DIR_PATH)
    except:
        print sys.exc_info()
        
    try:
        if os.path.exists(settings.DB_PATH):
            os.remove(settings.DB_PATH)
        init_db()
        if getpwuid(os.getuid())[0] == 'root':
            os.chown(settings.DB_PATH, apache_uid, apache_gid)
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
    """set admin password"""
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
