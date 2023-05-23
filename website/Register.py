from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user

from website.defs.Allforms import EmailForm

from flask_login import current_user
from .Models import User
from website import save_url_token
from website.defs.Sendmail import sendmail

from website.defs.Jsonlanguage import get_json_language


register_blueprint = Blueprint('Register', __name__)


@register_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = EmailForm()

    if form.validate_on_submit() and request.method == 'POST':
        Email = form.email.data
        user = User.query.filter_by(email=Email).first()
        language = request.cookies.get('language')

        if user:
            return redirect(url_for('Login.login', already='True', email=Email))

        if language == "UA":
            subject = "Будь ласка, підтвердьте свою електронну адресу"
        elif language == "EN":
            subject = "Please verify your email address"
        else:
            language = "NL"
            subject = "Verifieer uw email adres alstublieft"

        token = save_url_token.dumps(f"{Email}", salt='verifyemails')
        token_link = url_for('Register_token.register_token',
                             token=token, _external=True)

        html_body = render_template(
            'Verify_mail.html', action_url=token_link, language=language)
        sendmail(subject=subject, body=html_body, receiver=Email)

        return redirect(url_for('Register.register', sendmail=Email))

    return render_template('Register.html', user=current_user, form=form, language_dict=get_json_language())
