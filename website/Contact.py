from flask import Blueprint, render_template
from flask_login import current_user

from website.defs.Jsonlanguage import get_json_language


contact_blueprint = Blueprint('Contact', __name__)


@contact_blueprint.route('/contact', methods=['GET'])
def contact():
    return render_template('Contact.html', user=current_user, language_dict=get_json_language())