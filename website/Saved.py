from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user, login_required

from .Models import Cvformat
from website import db

from website.defs.Jsonlanguage import get_json_language


saved_blueprint = Blueprint('Saved', __name__)
savedask_blueprint = Blueprint('Savedask', __name__)


@login_required
@saved_blueprint.route('/saved', methods=['GET'])
def saved():
    return render_template('Saved.html', user=current_user, language_dict=get_json_language())



@login_required
@savedask_blueprint.route('/savedask', methods=['GET'])
def saved():
    accounts = request.args.get('profilesbycode')
    
    if not accounts:
        return [{}]
    
    account_list = accounts.split('-')[1:]
    account_list = [f'#{account}' for account in account_list]
    
    account_information = [Cvformat.query.filter_by(code=account_code).first().__dict__ for account_code in account_list]
    
    cleaned_list = []
    
    for posts in account_information:
        del posts['contact'], posts['user_id'], posts['_sa_instance_state'], posts['id']
        cleaned_list.append(posts)
        
    return jsonify(cleaned_list)
