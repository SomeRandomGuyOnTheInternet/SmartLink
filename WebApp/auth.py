import random
import functools
from flask import redirect, session, url_for

connected = False

def remote_required(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        if connected is True:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('find_remote'))
    return wrap

def generate_id():
    min = 0
    max = 99999999
    return "%05d" % random.randint(min, max)
