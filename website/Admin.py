import contextlib
from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_login import current_user, login_required

from werkzeug.security import generate_password_hash
from .Models import User, Cvformat, Employerformat, Likeformat, Dislikeformat
from website import db

from website.defs.Allforms import Amdinform, Adminemployer, Adminemployee
from website.defs.Admindecorator import admin_only
from website.defs.Jsonlanguage import get_json_language


admin_blueprint = Blueprint('Admin', __name__)
adminedit_blueprint = Blueprint('Adminedit', __name__)
admindelete_blueprint = Blueprint('Admindelete', __name__)


@admin_blueprint.route('/<view>/admin', methods=['GET'])
@login_required
@admin_only
def admin(view):
    if view == 'employees':
        users = Cvformat.query.all()
        return render_template('Adminemployeeview.html', user=current_user, employee_data=users, language_dict=get_json_language())

    elif view == 'employers':
        users = Employerformat.query.all()
        return render_template('Adminemployerview.html', user=current_user, employer_data=users, language_dict=get_json_language())
    else:
        users = User.query.all()
        amount_employers = sum(user.employer is True for user in users)
        return render_template('Admin.html', user=current_user, userdata=users, employer_length=amount_employers, language_dict=get_json_language())


@admin_blueprint.route('/admin/edit/<role>/<user_id>', methods=['GET', 'POST'])
@login_required
@admin_only
def adminedit(role, user_id):
    employer_form = Adminemployer()
    employee_form = Adminemployee()

    form = Amdinform()
    user = User.query.filter_by(id=user_id).first()

    if not form.validate_on_submit() and request.method != 'POST':
        form = add_value_to_user_account(form, user)

    if form.validate_on_submit() and request.method == 'POST':
        edit_user_account(form, user)
        employer_boolean = form.employer.data == 'employer'

        if employer_boolean:
            EMPLOYER = Employerformat.query.filter_by(user_id=user.id).first()
            edit_user_employer(employer_form, EMPLOYER)
        else:
            EMPLOYEE = Cvformat.query.filter_by(user_id=user.id).first()
            edit_user_employee(employee_form, EMPLOYEE)

            return redirect(url_for('Admin.admin', view='users'))

    if role == 'employer':
        EMPLOYER = Employerformat.query.filter_by(user_id=user.id).first()
        filled_employer_form = add_value_to_employer_account(
            employer_form, EMPLOYER)
        return render_template('Adminviewuser.html', user=current_user, view_user=user, role='employer', CV=EMPLOYER, form=form, employer_form=filled_employer_form, language_dict=get_json_language())
    else:
        EMPLOYEE = Cvformat.query.filter_by(user_id=user.id).first()
        filled_employee_form = add_value_to_employee_account(
            employee_form, EMPLOYEE)
        return render_template('Adminviewuser.html', user=current_user, view_user=user, role='employee', CV=EMPLOYEE, form=form, employee_form=filled_employee_form, employee_id=EMPLOYEE.id, language_dict=get_json_language())


@admindelete_blueprint.route('/admin/delete/<user_id>', methods=['GET'])
@login_required
@admin_only
def Admindelete(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return redirect(url_for('Admin.admin'))

    if user.employer is True:
        with contextlib.suppress(Exception):
            EMPLOYER = Employerformat.query.filter_by(user_id=user.id).first()
            db.session.delete(EMPLOYER)
    else:
        with contextlib.suppress(Exception):
            EMPLOYEE = Cvformat.query.filter_by(user_id=user.id).first()
            db.session.delete(EMPLOYEE)

    all_likes = Likeformat.query.filter_by(likes=user_id).all()
    all_dislikes = Dislikeformat.query.filter_by(dislikes=user_id).all()

    for likes in all_likes:
        db.session.delete(likes)

    for dislikes in all_dislikes:
        db.session.delete(dislikes)

    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('Admin.admin', view='users'))


def edit_user_account(form, user):
    user.id = form.userid.data
    user.ip = form.ip.data
    user.email = form.email.data

    user.employer = form.employer.data == 'employer'
    if user.password != form.password.data:
        user.password = generate_password_hash(
            form.password.data, method='sha256')

    db.session.add(user)
    db.session.commit()


def add_value_to_user_account(form, user):
    form.userid.data = user.id
    form.email.data = user.email
    form.password.data = user.password
    form.creationdate.data = user.create_date
    form.lastlogin.data = user.last_login
    form.employer.data = 'employer' if user.employer else 'employee'
    form.ip.data = user.ip
    return form


def add_value_to_employer_account(employer_form, EMPLOYER):
    employer_form.coins.data = EMPLOYER.coins
    employer_form.subscription.data = EMPLOYER.subscription
    employer_form.user_id.data = EMPLOYER.user_id
    return employer_form


def edit_user_employer(employer_form, EMPLOYER):
    EMPLOYER.coins = employer_form.coins.data
    EMPLOYER.subscription = employer_form.subscription.data
    EMPLOYER.user_id = employer_form.user_id.data

    db.session.add(EMPLOYER)
    db.session.commit()


def add_value_to_employee_account(employee_form, EMPLOYEE):

    employee_form.name.data = EMPLOYEE.name
    employee_form.age.data = EMPLOYEE.age
    employee_form.language.data = EMPLOYEE.language
    employee_form.region.data = EMPLOYEE.region
    employee_form.fulltime.data = 'Full-time' if EMPLOYEE.fulltime else 'Part-time'
    employee_form.schooling.data = EMPLOYEE.schooling
    employee_form.men.data = 'Men' if EMPLOYEE.men else 'Lady'
    employee_form.comment.data = EMPLOYEE.comment
    employee_form.contact.data = EMPLOYEE.contact

    employee_form.landbouw.data = EMPLOYEE.landbouw
    employee_form.bouw.data = EMPLOYEE.bouw
    employee_form.handel.data = EMPLOYEE.handel
    employee_form.gezondheidszorg.data = EMPLOYEE.gezondheidszorg
    employee_form.communicatie.data = EMPLOYEE.communicatie
    employee_form.onderwijs.data = EMPLOYEE.onderwijs
    employee_form.horeca.data = EMPLOYEE.horeca
    employee_form.transport.data = EMPLOYEE.transport
    employee_form.productie.data = EMPLOYEE.productie
    employee_form.engineering.data = EMPLOYEE.transport

    employee_form.outexperience.data = EMPLOYEE.outexperience
    employee_form.inexperience.data = EMPLOYEE.inexperience

    employee_form.currentlylooking.data = 'Yes' if EMPLOYEE.currentlylooking else 'No'
    return employee_form


def edit_user_employee(employee_form, EMPLOYEE):
    EMPLOYEE.name = employee_form.name.data
    EMPLOYEE.age = employee_form.age.data
    EMPLOYEE.language = employee_form.language.data
    EMPLOYEE.region = employee_form.region.data
    EMPLOYEE.fulltime = employee_form.fulltime.data == 'Full-time'
    EMPLOYEE.men = employee_form.men.data == 'Men'
    EMPLOYEE.contact = employee_form.contact.data
    EMPLOYEE.currentlylooking = employee_form.currentlylooking.data == 'Yes'
    EMPLOYEE.language = employee_form.language.data

    EMPLOYEE.comment = employee_form.comment.data
    EMPLOYEE.schooling = employee_form.schooling.data
    EMPLOYEE.inexperience = employee_form.inexperience.data
    EMPLOYEE.outexperience = employee_form.outexperience.data

    EMPLOYEE.landbouw = employee_form.landbouw.data
    EMPLOYEE.bouw = employee_form.bouw.data
    EMPLOYEE.handel = employee_form.handel.data
    EMPLOYEE.gezondheidszorg = employee_form.gezondheidszorg.data
    EMPLOYEE.communicatie = employee_form.communicatie.data
    EMPLOYEE.onderwijs = employee_form.onderwijs.data
    EMPLOYEE.horeca = employee_form.horeca.data
    EMPLOYEE.transport = employee_form.transport.data
    EMPLOYEE.productie = employee_form.productie.data
    EMPLOYEE.engineering = employee_form.engineering.data

    db.session.add(EMPLOYEE)
    db.session.commit()
