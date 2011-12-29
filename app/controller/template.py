# -*- encoding: utf-8 -*-
"""
    :copyright: (c) 2011 by daisuke igarashi.
"""
import os
import sys

from flask import (Blueprint, render_template, request, flash, abort, 
                   redirect, g, url_for, jsonify, session, current_app)

from app import forms, settings, utils
from app.models import TemplateModel, TagModel

mod = Blueprint('template', __name__, url_prefix='/template')

# pagination
PER_PAGE = 9

@mod.route("/", methods=["GET"], defaults={"page":1})
@mod.route("/page/<int:page>")
def list(page):
    g.ctx["is_active_home"] = True
    pagination = TemplateModel().get_pagination(page, PER_PAGE)
    return render_template("temp/list.html", pagination=pagination, **g.ctx)

@mod.route("/tag/<tagname>/", methods=["GET"], defaults={"page":1})
@mod.route("/tag/<tagname>/page/<int:page>")
def list_tag(tagname, page):
    tag = TagModel().get_tag(tagname) or abort(404)
    pagination = TemplateModel().get_list_tag_pagenation(page, PER_PAGE, tag)
    return render_template("temp/list.html", pagination=pagination, TAG_PAGE_TITLE="tag \""+tagname+"\" list", **g.ctx)

@mod.route("/show/<id>/", methods=["GET"])
def show(id):
    item = TemplateModel().get(id) or abort(404)
    return render_template("temp/show.html", item=item, **g.ctx)
    
@mod.route("/new/", methods=["GET", "POST"])
@utils.requires_admin
def new():
    form = forms.TemplateForm(request.form)

    if request.method == "GET":
        return render_template("temp/new.html", form=form, **g.ctx)

    if not form.validate_on_submit():
        utils.flash_errors(form.errors)
        return render_template("temp/new.html", form=form, **g.ctx)
    
    TemplateModel().new(form, g.user)
    
    return redirect(url_for("template.list"))

@mod.route("/edit/<id>/", methods=["GET", "POST"])
@utils.requires_admin
def edit(id):
    form = forms.EditTemplateForm(request.form)
    template = TemplateModel().get(id) or abort(404)
    g.ctx["form"] = form
    g.ctx["template"] = template
    
    if request.method == "GET":
        form.subject.data = template.subject
        form.description.data = template.description
        form.tags.data = [tag.name for tag in template.tags]
        return render_template("temp/edit.html", **g.ctx)

    if not form.validate_on_submit():
        utils.flash_errors(form.errors)
        return render_template("temp/edit.html", **g.ctx)

    TemplateModel().update(template, form, g.user)
    
    return redirect(url_for('template.show', id=id))

@mod.route("/delete/<id>/", methods=["POST"])
@utils.requires_admin
def delete(id):
    template = TemplateModel().get(id) or abort(404)
    TemplateModel().delete(template)
    return redirect(url_for('index'))
