# -*- encoding: utf-8 -*-
"""
    :copyright: (c) 2011 by daisuke igarashi.
"""
from functools import wraps

from flask import (
    Flask, session, g, redirect, url_for, session, request, flash, abort, current_app
    )

def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.signin', next=request.path))
        return f(*args, **kwargs)
    return decorated_function

def requires_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None or g.user.role.rolename != "admin":
            flash(u"管理者権限が必要です。")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def flash_errors(errors):
    for error in errors.values():
        for error_str in error:
            flash(error_str)

def format_datetime(dt_string):
    """
    >>> format_datetime("2011-01-20 12:20:30.12345")
    '2011-01-20 @ 12:20'
    """
    import datetime
    dt = datetime.datetime.strptime(dt_string, '%Y-%m-%d %H:%M:%S.%f')
    return dt.strftime('%Y-%m-%d @ %H:%M')

