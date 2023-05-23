from flask import Blueprint, render_template, jsonify, request
from flask_login import current_user, login_required

from .Models import User, Cvformat
from website import db

from sqlalchemy.sql import or_

from website.defs.Jsonlanguage import get_json_language


search_blueprint = Blueprint('Search', __name__)
searchask_blueprint = Blueprint('Searchask', __name__)


workname_list = (Cvformat.landbouw, Cvformat.bouw, Cvformat.handel, Cvformat.gezondheidszorg, Cvformat.communicatie, Cvformat.onderwijs, Cvformat.horeca, Cvformat.transport, Cvformat.productie, Cvformat.engineering)
    

@search_blueprint.route('/search', methods=['GET'])
def search():
    return render_template('Search.html', user=current_user, language_dict=get_json_language())


@login_required
@searchask_blueprint.route('/searchask', methods=['GET'])
def searchask():
    search = request.args.get('search')
    region = request.args.get('region')
    worktime = request.args.get('worktime')
    pagenumber = request.args.get('pagenumber')
    gender = request.args.get('gender')
    working = request.args.get('working')
    
    work_list = [
        request.args.get('landbouw') == 'true',
        request.args.get('bouw') == 'true',
        request.args.get('handel') == 'true',
        request.args.get('gezondheidszorg') == 'true',
        request.args.get('communicatie') == 'true',
        request.args.get('onderwijs') == 'true',
        request.args.get('horeca') == 'true',
        request.args.get('transport') == 'true',
        request.args.get('productie') == 'true',
        request.args.get('engineering') == 'true'
    ]
    
    query = db.session.query(Cvformat)   
    queries = []
    
    if gender is not None:
        gender = gender == 'Male'
        query = query.filter(Cvformat.men == gender)
        
    if working is not None:
        working = working == 'yessearching'
        query = query.filter(Cvformat.currentlylooking == working)
    
    if search is not None:
        query = query.filter(Cvformat.comment.like(f'%{search}%') | Cvformat.outexperience.like(f'%{search}%') | Cvformat.inexperience.like(f'%{search}%'))
    
    if any(work_list):
        queries.extend(name == work_bool for name, work_bool in zip(workname_list, work_list) if work_bool)
    query = query.filter(or_(*queries))
    
    if region is not None:
        query = query.filter(Cvformat.region == region)
    
    if worktime is not None:
        fulltime_boolian = worktime == 'Full-Time'
        query = query.filter(Cvformat.fulltime == fulltime_boolian)    
        
    try:
        pages_posts = query.paginate(int(pagenumber), 10, False).items
    except TypeError:
        pages_posts = query.paginate(1, 10, False).items
        
    cleaned_list = []
    
    for posts in pages_posts:
        temp_dict = vars(posts)
        del temp_dict['contact'], temp_dict['user_id'], temp_dict['_sa_instance_state'], temp_dict['id']
        if temp_dict['name'] != '':
            cleaned_list.append(temp_dict)
        
    return jsonify(cleaned_list)



