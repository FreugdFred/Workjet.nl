from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import current_user, login_user, logout_user

from website.defs.Allforms import Loginform

from flask_login import current_user
from .Models import User
from website import db

from werkzeug.security import check_password_hash
from sqlalchemy.sql import func

from website.defs.Jsonlanguage import get_json_language


login_blueprint = Blueprint('Login', __name__)
logout_blueprint = Blueprint('Logout', __name__)


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():  # sourcery skip: remove-unnecessary-else, swap-if-else-branches
    form = Loginform()
    
    if current_user.is_authenticated:
        return redirect(url_for('Profile.profile')) 
    
    if form.validate_on_submit() and request.method == 'POST':

        Email = form.email.data
        Password = form.password.data
        
        user = User.query.filter_by(email=Email).first()
        if not user:
            return redirect(url_for('Register.register', email=Email)) 
        
        if check_password_hash(user.password, Password):
            user.last_login = func.now()
            db.session.add(user)
            db.session.commit()
            
            login_user(user, remember=True)   
            return redirect(url_for('Profile.profile')) 
            
        else:
            return redirect(url_for('Login.login', email=Email, hidden='False')) 
        
    return render_template('Login.html', user=current_user, form=form, language_dict=get_json_language())


@logout_blueprint.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('Login.login'))