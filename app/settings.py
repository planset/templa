# -*- encoding: utf-8 -*-
"""
    :copyright: (c) 2011 by daisuke igarashi.
"""
import os

# change it
SECRET_KEY = "\xa5\xfc\x83X\x86tcX\x18;\xb2\x81\xa2$\xae$\x12\r'\xcd\x06\x83HT"

# save user uploaded files
DATA_DIR_NAME = "data"

# save thumbnail images
THUMBNAIL_DIR_NAME = "thumbnail"

# expand compressed template to this directory
DEMO_DIR_NAME = "static_demo"

# database file name
DB_NAME = "templa.db"

# abs path settings.py 
CUR_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR_PATH = os.path.join(CUR_DIR, DATA_DIR_NAME)
DEMO_DIR_PATH = os.path.join(CUR_DIR, DEMO_DIR_NAME)
THUMBNAIL_DIR_PATH = os.path.join(CUR_DIR, "static", THUMBNAIL_DIR_NAME)
DB_PATH = os.path.join(CUR_DIR, DB_NAME)

DB_CONFIG = "sqlite:///" + DB_PATH

del os
