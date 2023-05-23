from flask import Blueprint, render_template
from flask_login import current_user

from website.defs.Jsonlanguage import get_json_language


errorpage_blueprint = Blueprint('errors', __name__)


@errorpage_blueprint.app_errorhandler(404)
def handle_404(err):
    return render_template('404.html', user=current_user, error_text=err, language_dict=get_json_language()), 404


@errorpage_blueprint.app_errorhandler(500)
def handle_500(err):
    return render_template('500.html', user=current_user, error_text=err, language_dict=get_json_language()), 500