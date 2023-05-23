from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import current_user, login_required

from website.defs.Allforms import EmailForm, ResetpasswordForm

from itsdangerous import SignatureExpired, BadTimeSignature
from werkzeug.security import generate_password_hash
from flask_login import current_user
from .Models import User, Cvformat
from website import save_url_token, db
from website.defs.Sendmail import sendmail

from .Models import User


from website.defs.Jsonlanguage import get_json_language


forgotpassword_blueprint = Blueprint('Forgotpassword', __name__)
forgotpassword_token_blueprint = Blueprint(
    'Tokenforgotpasswordtoken', __name__)


@forgotpassword_blueprint.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
    form = EmailForm()

    if form.validate_on_submit() and request.method == 'POST':
        Email = form.email.data
        user = User.query.filter_by(email=Email).first()
        language = request.cookies.get('language')

        if language == "UA":
            subject = "Скинути пароль"
        elif language == "EN":
            subject = "Reset you password"
        else:
            language = "NL"
            subject = "reset je wachtwoord"

        if user:
            token = save_url_token.dumps(f"{Email}", salt='resetthepassword')
            token_link = url_for(
                'forgotpasswordtoken.tokenforgotpassword', token=token, _external=True)

            html_body = render_template(
                'Resetpassword_mail.html', action_url=token_link, language=language)
            sendmail(subject=subject, body=html_body, receiver=Email)

        return redirect(url_for('Forgotpassword.forgotpassword', email=Email))

    return render_template('Forgotpassword.html', user=current_user, form=form, language_dict=get_json_language())


@forgotpassword_token_blueprint.route('/forgotpassword/<token>', methods=['POST', "GET"])
def tokenforgotpassword(token):
    try:
        Email = save_url_token.loads(
            token, salt='resetthepassword', max_age=1200)
        user = User.query.filter_by(email=Email).first()
        form = ResetpasswordForm()

        if not user:
            return redirect(url_for('Register.register', email=Email))

        if form.validate_on_submit() and request.method == 'POST':
            Password = form.password.data

            user.password = generate_password_hash(Password, method='sha256')
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('Login.login', email=Email))

        return render_template('Registertoken.html', password='forgot',  user=current_user, form=form, language_dict=get_json_language())

    except SignatureExpired:
        return render_template('Errorpage.html', text="Sorry, this token is expired, Deze link is verlopen, термін дії цього посилання закінчився", user=current_user, language_dict=get_json_language())

    except BadTimeSignature:
        return render_template('Errorpage.html', text="Sorry, this token does not exist, Deze link bestaat niet, цього посилання не існує", user=current_user, language_dict=get_json_language())
