# -*- encoding: utf-8 -*-
"""
    :copyright: (c) 2011 by daisuke igarashi.
"""
import os
import sys

from flask import (
    Flask, flash, abort, session, g, redirect, url_for, 
    session, request, render_template, send_from_directory)
from flask.ext.sqlalchemy import SQLAlchemy

from app import forms, settings, utils
from app.db import db_session, Template, User, UserRole, Tag
from app.models import TemplateModel, UserModel, UserRoleModel
from app.lib.thumbnail import Thumbnail, ThumbnailSize


app = Flask(__name__)
app.config.from_pyfile("settings.py")


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

@app.before_request
def set_default_ctx():
    g.ctx = {}

@app.before_request
def check_user():
    g.user = None
    user_id = session.get("user_id")
    if user_id:
        g.user = User.query.get(user_id)
    if g.user is None:
        login_form = forms.SigninForm()
        login_form.next.data = request.url
        g.ctx["login_form"] = login_form

@app.before_request
def load_tags():
    tags = Tag.query.all()
    g.ctx["tags"] = tags

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
    
@app.route("/")
def index():
    return redirect(url_for("template.list"))

@app.route("/demo/<path:path>")
def send_demo(path):
    return send_from_directory(settings.DEMO_DIR_PATH, path)

@app.route("/archive/<path:filename>")
def send_archive(filename):
    return send_from_directory(settings.DATA_DIR_PATH, filename, as_attachment=True)



app.jinja_env.filters['format_datetime'] = utils.format_datetime

def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)

app.jinja_env.globals['url_for_other_page'] = url_for_other_page

def get_main_thumbnail_filename(template_id):
    t = Thumbnail(settings.CUR_DIR, settings.THUMBNAIL_DIR_NAME)
    if not os.path.exists(t.get_thumbnail_path(str(template_id), ThumbnailSize.medium)):
        return "noimage.png"
    return t.get_thumbnail_name(str(template_id), ThumbnailSize.medium)
    
app.jinja_env.globals['get_main_thumbnail_filename'] = get_main_thumbnail_filename

def get_big_thumbnail_filename(template_id):
    t = Thumbnail(settings.CUR_DIR, settings.THUMBNAIL_DIR_NAME)
    if not os.path.exists(t.get_thumbnail_path(str(template_id), ThumbnailSize.big)):
        return"noimage.png"
    return t.get_thumbnail_name(str(template_id), ThumbnailSize.big)
    
app.jinja_env.globals['get_big_thumbnail_filename'] = get_big_thumbnail_filename

def get_demo_url(template_id, index_filename):
    demo_filename = str(template_id) + "/" + index_filename
    if not os.path.exists(os.path.join(settings.CUR_DIR, settings.DEMO_DIR_NAME, demo_filename)):
        return "#"
    return url_for('send_demo', path=demo_filename)

app.jinja_env.globals['get_demo_url'] = get_demo_url

def get_archive_url(template_id, filename):
    archive_filename = str(template_id) + "/" + filename
    filepath=os.path.join(settings.CUR_DIR, settings.DATA_DIR_NAME, archive_filename)
    if not os.path.exists(filepath):
        return "#"
    return url_for('send_archive', filename=archive_filename)

app.jinja_env.globals['get_archive_url'] = get_archive_url


from controller import auth
from controller import template
app.register_blueprint(auth.mod)
app.register_blueprint(template.mod)


if __name__ == "__main__":
    app.run(debug=True)



