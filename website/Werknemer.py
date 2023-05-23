from flask import Blueprint, render_template
from flask_login import current_user, login_required

from website.defs.Jsonlanguage import get_json_language

werknemer_blueprint = Blueprint('Werknemer', __name__)


@werknemer_blueprint.route('/werknemer', methods=['GET'])
def werknemer():
    return render_template('Werknemer.html', user=current_user, language_dict=get_json_language())