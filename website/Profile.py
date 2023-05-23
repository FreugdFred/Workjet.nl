from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required

from website.defs.Allforms import Cvform

from flask_login import current_user
from .Models import User, Cvformat, Employerformat
from website import db

from website.defs.Jsonlanguage import get_json_language

from deep_translator import (GoogleTranslator, DeeplTranslator)


profile_blueprint = Blueprint('Profile', __name__)
deleteprofile_blueprint = Blueprint('Deleteprofile', __name__)


@profile_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.employer:
        user_employer = Employerformat.query.filter_by(user_id=current_user.id).first()
        return render_template('Employerprofile.html', user=current_user, employer=user_employer, language_dict=get_json_language())
         
    form = Cvform() 
    user_cv = Cvformat.query.filter_by(user_id=current_user.id).first()
    
    if not form.validate_on_submit()  and request.method != 'POST':
        form  = add_value_to_form_employee(form, user_cv)

    if form.validate_on_submit() and request.method == 'POST':
        add_value_to_employee_profile(form, user_cv)
        
        return redirect(url_for('Home.home', profile='updated')) 

    return render_template('Profile.html', user=current_user, form=form, language_dict=get_json_language())


@profile_blueprint.route('/deleteprofile', methods=['GET', 'POST'])
@login_required
def deleteprofile():
    user_cv = Cvformat.query.filter_by(user_id=current_user.id).first()
    
    user_cv.name = ''
    user_cv.age = ''
    user_cv.language = ''
    user_cv.region = ''
    user_cv.fulltime = True
    user_cv.schooling = ''
    user_cv.men = True
    user_cv.comment = ''
    user_cv.contact = ''
    user_cv.outexperience = ''
    user_cv.inexperience = ''
    
    user_cv.landbouw = False
    user_cv.bouw = False
    user_cv.handel = False
    user_cv.gezondheidszorg = False 
    user_cv.communicatie = False 
    user_cv.onderwijs = False 
    user_cv.horeca = False
    user_cv.transport = False 
    user_cv.engineering = False 
    
    user_cv.currentlylooking = False 
    
    db.session.add(user_cv)
    db.session.commit()
    
    return '{}'



def add_value_to_form_employee(form, user_cv):
    form.name.data = user_cv.name
    form.age.data = user_cv.age
    form.language.data = user_cv.language
    form.region.data = user_cv.region
    form.fulltime.data = 'Full-time' if user_cv.fulltime else 'Part-time'
    form.schooling.data = user_cv.schooling
    form.men.data = 'Men' if user_cv.men else 'Lady'
    form.comment.data = user_cv.comment
    form.contact.data = user_cv.contact
    
    form.landbouw.data = user_cv.landbouw
    form.bouw.data = user_cv.bouw
    form.handel.data = user_cv.handel
    form.gezondheidszorg.data = user_cv.gezondheidszorg
    form.communicatie.data = user_cv.communicatie
    form.onderwijs.data = user_cv.onderwijs
    form.horeca.data = user_cv.horeca
    form.transport.data = user_cv.transport
    form.productie.data = user_cv.productie
    form.engineering.data = user_cv.transport
    
    form.outexperience.data = user_cv.outexperience
    form.inexperience.data = user_cv.inexperience
    
    form.currentlylooking.data = 'Yes' if user_cv.currentlylooking else 'No'
    
    return form


def add_value_to_employee_profile(form, user_cv):
    user_cv.name = form.name.data
    user_cv.age = form.age.data
    user_cv.language = form.language.data
    user_cv.region = form.region.data
    user_cv.fulltime = form.fulltime.data == 'Full-time'
    user_cv.men = form.men.data == 'Men'
    user_cv.contact = form.contact.data
    user_cv.currentlylooking = form.currentlylooking.data == 'Yes'
    user_cv.language = form.language.data
            
    try:
        user_cv.comment = GoogleTranslator(target='nl').translate(form.comment.data)
        user_cv.schooling = GoogleTranslator(target='nl').translate(form.schooling.data)
        user_cv.inexperience = GoogleTranslator(target='nl').translate(form.inexperience.data)
        user_cv.outexperience = GoogleTranslator(target='nl').translate(form.outexperience.data)
    except Exception:
        try:
            user_cv.comment = DeeplTranslator(target='nl').translate(form.comment.data)
            user_cv.schooling = DeeplTranslator(target='nl').translate(form.schooling.data)
            user_cv.inexperience = DeeplTranslator(target='nl').translate(form.inexperience.data)
            user_cv.outexperience = DeeplTranslator(target='nl').translate(form.outexperience.data)
        except Exception:
            user_cv.comment = form.comment.data
            user_cv.schooling = form.schooling.data
            user_cv.inexperience = form.inexperience.data
            user_cv.outexperience = form.outexperience.data
        
    user_cv.landbouw = form.landbouw.data
    user_cv.bouw = form.bouw.data
    user_cv.handel = form.handel.data
    user_cv.gezondheidszorg = form.gezondheidszorg.data
    user_cv.communicatie = form.communicatie.data
    user_cv.onderwijs = form.onderwijs.data
    user_cv.horeca = form.horeca.data
    user_cv.transport = form.transport.data
    user_cv.productie = form.productie.data
    user_cv.engineering = form.engineering.data
    
    db.session.add(user_cv)
    db.session.commit()