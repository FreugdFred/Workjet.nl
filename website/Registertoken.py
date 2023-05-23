from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user

from website.defs.Allforms import PasswordForm

from itsdangerous import SignatureExpired, BadTimeSignature
from werkzeug.security import generate_password_hash
from flask_login import current_user
from .Models import User, Cvformat, Employerformat
from website import save_url_token, db
from website.defs.Sendmail import sendmail
from website.defs.Randomstring import get_random_string

from website.defs.Jsonlanguage import get_json_language


register_token_blueprint = Blueprint('Register_token', __name__)


@register_token_blueprint.route('/register/<token>', methods=['GET', 'POST'])
def register_token(token):
    try:
        Email = save_url_token.loads(token, salt='verifyemails', max_age=1200)
        user = User.query.filter_by(email=Email).first()
        form = PasswordForm()

        if user:
            return redirect(url_for('Home.home'))

        if form.validate_on_submit() and request.method == 'POST':   
            Password = form.password.data
            BoolEmployer = form.employer.data == 'employer'

            new_user = User(email=Email, password=generate_password_hash(Password, method='sha256'), ip=request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr), employer=BoolEmployer)
            db.session.add(new_user)
            db.session.commit()

            user = User.query.filter_by(email=Email).first()
            
            if BoolEmployer:
                Employer_info = Employerformat(user_id=user.id)
                db.session.add(Employer_info)
                
            else:
                cv_info = Cvformat(user_id=user.id, code=f'#{get_random_string()}')
                db.session.add(cv_info)
                
            db.session.commit()

            return redirect(url_for('Login.login', email=Email)) 

        return render_template('Registertoken.html', user=current_user, form=form, language_dict=get_json_language())

    except SignatureExpired:
        return render_template('Errorpage.html', text="Sorry, this token is expired, Deze link is verlopen, термін дії цього посилання закінчився", user=current_user, language_dict=get_json_language())

    except BadTimeSignature:
        return render_template('Errorpage.html', text="Sorry, this token does not exist, Deze link bestaat niet, цього посилання не існує", user=current_user, language_dict=get_json_language())