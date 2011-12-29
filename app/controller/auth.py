# -*- encoding: utf-8 -*-
"""
    :copyright: (c) 2011 by daisuke igarashi.
"""
from flask import (Blueprint, render_template, request, flash, abort, 
                   redirect, g, url_for, jsonify, session, current_app)

from app import forms, utils

mod = Blueprint('auth', __name__, url_prefix='/auth')

@mod.route("/", methods=["POST"])
def signin():
    form = forms.SigninForm(request.form)
    next_url = form.next.data or url_for('index')
    
    if not form.validate_on_submit():
        utils.flash_errors(form.errors)
        return redirect(next_url)
    
    session['user_id'] = form.user.id
    return redirect(next_url)

@mod.route("/logout/")
def logout():
    if "user_id" in session:
        del session["user_id"]
    next_url = url_for('index')#request.args.get("next_url") or request.headers["Referer"] or url_for('index')
    return redirect(next_url)
