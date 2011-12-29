# -*- encoding: utf-8 -*-
"""
    :copyright: (c) 2011 by daisuke igarashi.
"""
import os
import shutil
import datetime

from werkzeug import secure_filename
from flask.ext.sqlalchemy import Pagination
from sqlalchemy import or_, and_, desc

from app.db import db_session, Template, User, UserRole, Tag
from app.lib import myzip, thumbnail, webscreenshot
from app import settings

def uncompress_template(template_id, filename):
    demo_dirpath = os.path.join(settings.DEMO_DIR_PATH, str(template_id))
    if not os.path.exists(demo_dirpath):
        os.mkdir(demo_dirpath)
    archive_filepath = get_save_filepath(template_id, filename)
    os.system(" ".join(["unzip", "-u", archive_filepath, "-d", demo_dirpath]))

def make_thumbnail(template_id, index_filename):
    demo_dirpath = os.path.join(settings.DEMO_DIR_PATH, str(template_id))
    html_filepath = os.path.join(demo_dirpath,
                                 index_filename)
    image_filename = str(template_id) + "_" + "original.png"
    image_filepath = os.path.join(settings.THUMBNAIL_DIR_PATH,
                                  image_filename)
    webscreenshot.save1280x720(html_filepath, image_filepath)
    
    if os.path.exists(image_filepath):
        t = thumbnail.Thumbnail(settings.CUR_DIR, settings.THUMBNAIL_DIR_NAME)
        t.from_file(image_filepath)
        t.saveall(str(template_id))
        os.remove(image_filepath)
    
    return

def get_save_dirpath(template_id):
    return os.path.join(settings.DATA_DIR_PATH, str(template_id))

def get_save_filepath(template_id, filename):
    dir_path = get_save_dirpath(template_id)
    return os.path.join(dir_path, filename)

def save_template_file(template_id, form_file, filename):
    dir_path = get_save_dirpath(template_id)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    filepath = get_save_filepath(template_id, filename)
    form_file.save(filepath)
    return myzip.get_fileinfo(filepath)
    
def rmtree(path):
    if os.path.exists(path):
        shutil.rmtree(path)

def delete_template_files(id):
    rmtree(os.path.join(settings.DATA_DIR_PATH, str(id)))
    rmtree(os.path.join(settings.DEMO_DIR_PATH, str(id)))
    for size in thumbnail.THUMBNAIL_SIZE_DICT.keys():
        p = os.path.join(settings.THUMBNAIL_DIR_PATH, str(id)+"_"+size+".jpg")
        if os.path.exists(p):
            os.remove(p)

class TemplateModel(object):
    def get(self, id):
        return Template.query.get(id)

    def get_pagination(self, page, per_page):
        items = Template.query.order_by(desc(Template.create_date)).limit(per_page).offset((page - 1) * per_page).all()
        return Pagination(Template.query, page, per_page, Template.query.count(), items)

    def get_list_tag_pagenation(self, page, per_page, tag):
        items = Template.query.filter(Template.tags.contains(tag)).order_by(desc(Template.create_date)).limit(per_page).offset((page - 1) * per_page).all()
        return Pagination(Template.query, page, per_page, self.get_list_tag_count(tag), items)

    def get_list_tag_count(self, tag):
        return Template.query.filter(Template.tags.contains(tag)).count()

    def new(self, form, user):
        filename = secure_filename(form.archive.file.filename)

        # add Template to db
        newtemp = Template(form.subject.data, 
                           user,
                           filename,
                           len(form.archive.file.stream.getvalue())/1024,
                           description=form.description.data,
                           tags=form.tags.data
                           )
        if not newtemp:
            flash("db error")
            abort(401)
        
        db_session.add(newtemp)
        db_session.commit()

        fileinfo = save_template_file(newtemp.id, form.archive.file, filename)
        newtemp.compressed_filelist = fileinfo.compressed_filelist
        newtemp.index_filename = fileinfo.index_filename
        db_session.commit()
    
        uncompress_template(newtemp.id, filename)
        make_thumbnail(newtemp.id, newtemp.index_filename)
    
    def update(self, template, form, user):
        filename = secure_filename(form.archive.file.filename)
    
        template.subject = form.subject.data
        template.description = form.description.data
        template.tags = []
        for tag_name in form.tags.data:
            tag = Tag.query.filter(Tag.name==tag_name).first() or Tag(tag_name)
            template.tags.append(tag)
        template.modified_date = datetime.datetime.now()

        if len(filename) > 0:
            delete_template_files(template.id)
            
            template.filename = filename
            fileinfo = save_template_file(template.id, form.archive.file, filename)
            template.compressed_filelist = fileinfo.compressed_filelist
            template.index_filename = fileinfo.index_filename

            uncompress_template(template.id, filename)
            make_thumbnail(template.id, template.index_filename)

        db_session.add(template)
        db_session.commit()

    def delete(self, template):
        db_session.delete(template)
        db_session.commit()
        delete_template_files(template.id)
        TagModel().delete_having_no_template()
        
class UserRoleModel(object):
    def get_userrole(self, rolename):
        return db_session.query(UserRole).all()

class UserModel(object):
    def get(self, id):
        return User.query.get(id)
    def get_by_username(self, username):
        return User.query.filter(User.username==username).first()


class TagModel(object):
    def get_tag(self, tagname):
        return Tag.query.filter(Tag.name==tagname).first()
    def delete_having_no_template(self):
        items = Tag.query.all()
        for item in items:
            if len(item.templates)==0:
                db_session.delete(item)
        db_session.commit()
        
