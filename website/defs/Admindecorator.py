from functools import wraps
from flask import redirect, url_for
from flask_login import current_user

import datetime


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.email != 'REDACTED':
            return redirect(url_for('Profile.profile'))
        # print(f'\033[93mUser: {current_user.email} got in the admin page, date: {datetime.datetime.now()}\033[0m')
        return f(*args, **kwargs)
    return decorated_function




