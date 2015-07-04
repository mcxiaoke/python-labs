# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

import hashlib
from base64 import b64encode


def make_hash(username, secret, password):
    """Generate a salt and return a new hash for the password."""
    if isinstance(password, unicode):
        password = password.encode('utf-8')
    salt = b64encode(username + secret)
    print 'make_hash,salt=', salt
    result = hashlib.sha256()
    result.update(password)
    print 'make_hash,result=', result.hexdigest()
    return result.hexdigest()


def check_hash(username, secret, password, hash):
    """Check a password against an existing hash."""
    return make_hash(username, secret, password) == hash

