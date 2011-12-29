from flaskext.wtf import (Form, TextField, TextAreaField, Required, 
                         Length, PasswordField, FileField, file_allowed,
                         file_required, HiddenField, SelectField, SubmitField,
                         FieldList)
from flaskext.wtf import (ValidationError)
# -*- encoding: utf-8 -*-
"""
    :copyright: (c) 2011 by daisuke igarashi.
"""
from wtforms.fields import Field
from wtforms.validators import StopValidation
from wtforms.widgets import (Select, TextInput)
from flaskext.uploads import UploadSet, ARCHIVES

from app import settings
from app.models import UserModel
from app.lib.mypassword import get_password_hash


archives = UploadSet("archives", ARCHIVES)


class SigninForm(Form):
    next = HiddenField(u"next")
    username = TextField(u"username", validators=[
                Required(u"username is required")
            ],
            default="")
    password = PasswordField(u"password", validators=[
            ])
    submit = SubmitField(u"Sign in")
    
    def validate_password(form, field):
        user = UserModel().get_by_username(form.username.data) 
        if user is None:
            raise ValidationError("auth error")
        entry_password = get_password_hash(settings.SECRET_KEY, user.username, field.data)
        if entry_password != user.password:
            raise ValidationError("auth error")
        form.user = user


class TagListField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            return u", ".join(self.data)
        else:
            return u""

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',') if len(x.strip())>0]
        else:
            self.data = []

class TemplateForm(Form):
    subject = TextField(u"subject", validators=[
                Required(u"subject is required")
            ],
            default="")
    description = TextAreaField(u"description", validators=[
            ],
            default="")
    tags = TagListField(u"tag", validators=[
            ])
    archive = FileField(u"Template file", validators=[
                file_required(u"Template file is required"),
            ])
    submit = SubmitField(u"Add template")
        
    def validate_archive(form, field):
        if len(field.file.filename)>0 \
               and field.file.filename.split(".")[-1].upper() != "ZIP":
            raise ValidationError("archive is required compressed zip")

class EditTemplateForm(Form):
    subject = TextField(u"subject", validators=[
                Required(u"subject is required")
            ],
            default="")
    description = TextAreaField(u"description", validators=[
            ],
            default="")
    tags = TagListField(u"tag", validators=[
            ])
    archive = FileField(u"Template file", validators=[
            ])           
    cancel = SubmitField(u"Cancel")
    submit_update = SubmitField(u"Update")

    def validate_archive(form, field):
        if len(field.file.filename)>0 \
                and field.file.filename.split(".")[-1].upper() != "ZIP":
            raise ValidationError("archive is required compressed zip")


