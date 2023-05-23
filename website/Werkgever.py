from flask import Blueprint, render_template
from flask_login import current_user, login_required

from website.defs.Jsonlanguage import get_json_language


werkgever_blueprint = Blueprint('Werkgever', __name__)


@werkgever_blueprint.route('/werkgever', methods=['GET'])
def werkgever():
    return render_template('Werkgever.html', user=current_user, language_dict=get_json_language())