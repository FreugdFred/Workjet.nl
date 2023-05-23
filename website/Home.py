from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_login import current_user, login_required

from website.defs.Jsonlanguage import get_json_language

home_blueprint = Blueprint('Home', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template('Home.html', user=current_user, language_dict=get_json_language())
