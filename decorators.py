import logging

from functools import wraps
from flask import session, request, redirect, url_for

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'admin' not in session:
            logging.debug(request.url)
            return redirect(url_for('signin'))
        return f(*args, **kwargs)
    return wrapper
