from flask import Blueprint, render_template
from flask_login import current_user, login_required

from website.defs.Jsonlanguage import get_json_language


faq_blueprint = Blueprint('Faq', __name__)


@faq_blueprint.route('/faq', methods=['GET'])
def faq():
    return render_template('Faq.html', user=current_user, language_dict=get_json_language())