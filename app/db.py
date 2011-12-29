# -*- encoding: utf-8 -*-
"""
    :copyright: (c) 2011 by daisuke igarashi.
"""
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base
from app.settings import DB_CONFIG, SECRET_KEY

from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Binary, Float, BigInteger
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.expression import asc, desc

import datetime
import os

from app.lib.mypassword import get_password_hash

db_engine = create_engine(DB_CONFIG, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=db_engine))

Base = declarative_base()
Base.query = db_session.query_property()


class TagRelationships(Base):
    __tablename__ = 'tag_relationships'
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)
    template_id = Column(Integer, ForeignKey("templates.id"), primary_key=True)
    tag = relationship("Tag", primaryjoin="TagRelationships.tag_id==Tag.id")
    template = relationship("Template", primaryjoin="TagRelationships.template_id==Template.id")

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(), nullable=False, unique=True)
    templates = relationship("TagRelationships")
    
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return "<Tag {0}: {1}>".format(self.id, self.name)

class Template(Base):
    __tablename__ = 'templates'
    id = Column(Integer, primary_key=True)
    subject = Column(String(), nullable=False)
    description = Column(String(), nullable=False)
    url = Column(String(), nullable=False)
    filename = Column(String(), nullable=False)
    user_id = Column(Integer(), ForeignKey("users.id"), nullable=False)
    user = relationship("User", lazy='joined', innerjoin=False)
    compressed_filelist = Column(Binary(), nullable=False)
    filesize = Column(BigInteger(), nullable=False)     # in KB
    index_filename = Column(String(), nullable=False)
    tags = relationship(Tag, secondary="tag_relationships")
    thumbnail_count = Column(Integer(), nullable=False)
    create_date = Column(String(10), nullable=False, default=datetime.datetime.now())
    modified_date = Column(String(10), nullable=False, default=datetime.datetime.now())
    
    def __init__(self, subject, user, filename, filesize, tags='', description='', url='', 
                 compressed_filelist='', index_filename=''):
        super(Template, self).__init__()
        self.subject = subject
        self.filename = filename
        self.filesize = filesize
        self.user = user
        self.description = description
        self.url = url
        self.compressed_filelist = compressed_filelist
        self.index_filename = index_filename
        self.thumbnail_count = 0
        for tag_name in tags:
            tag = Tag.query.filter(Tag.name==tag_name).first() or Tag(tag_name)
            self.tags.append(tag)
    
    def get_filelist(self):
        import zlib
        import json
        try:
            return json.loads(zlib.decompress(self.compressed_filelist))
        except:
            return []
        
    def __repr__(self):
        return '<Template %r>' % (self.subject)

class UserRole(Base):
    __tablename__ = 'userroles'
    rolename = Column(String(), nullable=False, primary_key=True)
    description = Column(String(), nullable=False)
    users = relationship("User",
    primaryjoin="User.rolename==UserRole.rolename", back_populates="role")
    
    def __init__(self, rolename, description=''):
        super(UserRole, self).__init__()
        self.rolename = rolename
        self.description = description

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    rolename = Column(String(), ForeignKey("userroles.rolename"),
    nullable=False)
    role = relationship("UserRole", innerjoin=False)
    templates = relationship("Template",
        backref='users',
        primaryjoin="User.id==Template.user_id", 
        order_by="Template.create_date", 
        lazy='joined')
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(), nullable=False, default='')
    twitter_id = Column(String(), nullable=False)
    facebook_id = Column(String(), nullable=False)
    quote = Column(Float(), nullable=False, default=10.0)
    datasize = Column(Float(), nullable=False, default=0.0)
    email = Column(String(120), nullable=False)#, unique=True)
    create_date = Column(String(10), nullable=False, default=datetime.datetime.now())

    def __init__(self, username, role, password='', twitter_id='', facebook_id='', email=''):
        super(User, self).__init__()
        self.username = username
        self.role = role
        self.set_password(password)
        self.twitter_id = twitter_id
        self.facebook_id = facebook_id
        self.email = email

    def set_password(self, password):
        self.password = get_password_hash(SECRET_KEY, self.username, password)


def init_db():
    Base.metadata.create_all(bind=db_engine)

def session_remove():
    db_session.remove()


