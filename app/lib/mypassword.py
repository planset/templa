# -*- encoding: utf-8 -*-
"""
    :copyright: (c) 2011 by daisuke igarashi.
"""

import hmac
import hashlib


def get_password_hash(secretkey, username, password, salt='', stretchcount=10):
    password_hash = ""
    for i in range(stretchcount):
        password_hash = hmac.new(secretkey, password_hash + username + password + salt, hashlib.sha256).hexdigest()
    return password_hash
