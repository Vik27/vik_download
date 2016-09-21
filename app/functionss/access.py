from flask import session, flash, redirect, url_for, g, request
from functools import wraps
from flask.ext.login import logout_user

def log_required1(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not g.user.is_anonymous:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('root'))
    return wrap


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if g.user.role not in roles:
                logout_user()
                return redirect(url_for('root'))
            return f(*args, **kwargs)
        return wrapped
    return wrapper


def business_check(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        a = str(request.path).find('businesses/')
        businessId = int(str(request.path)[a+11])
        if not ((g.user.businessId == businessId) or (g.user.role == 'Admin')):
            logout_user()
            return redirect(url_for('root'))
        return f(*args, **kwargs)
    return wrapped