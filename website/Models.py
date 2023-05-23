from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Likeformat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    likes = db.Column(db.Integer)

    blog_id = db.Column(db.Integer)


class Dislikeformat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dislikes = db.Column(db.Integer)

    blog_id = db.Column(db.Integer)


class Blogformat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(400), default='None')
    post_text = db.Column(db.String(5000), default='None')
    post_creator = db.Column(db.String(100), default='None')
    post_date = db.Column(db.DateTime(timezone=True), default=func.now())


class Employerformat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coins = db.Column(db.Integer, default=0)
    subscription = db.Column(db.String(100), default='No')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Cvformat(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(db.String(100), default='#777')
    name = db.Column(db.String(100), default='')
    age = db.Column(db.Integer, default=0)
    language = db.Column(db.String(100), default='')
    region = db.Column(db.String(100), default='')
    fulltime = db.Column(db.Boolean, default=True)
    schooling = db.Column(db.String(100), default='')
    men = db.Column(db.Boolean, default=True)
    comment = db.Column(db.String(700), default='')
    contact = db.Column(db.String(100), default='')

    landbouw = db.Column(db.Boolean, default=False)
    bouw = db.Column(db.Boolean, default=False)
    handel = db.Column(db.Boolean, default=False)
    gezondheidszorg = db.Column(db.Boolean, default=False)
    communicatie = db.Column(db.Boolean, default=False)
    onderwijs = db.Column(db.Boolean, default=False)
    horeca = db.Column(db.Boolean, default=False)
    transport = db.Column(db.Boolean, default=False)
    productie = db.Column(db.Boolean, default=False)
    engineering = db.Column(db.Boolean, default=False)

    currentlylooking = db.Column(db.Boolean, default=False)
    outexperience = db.Column(db.String(500), default='')
    inexperience = db.Column(db.String(500), default='')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    create_date = db.Column(db.DateTime(timezone=True), default=func.now())
    last_login = db.Column(db.DateTime(timezone=True), default=func.now())
    employer = db.Column(db.Boolean, default=False)
    ip = db.Column(db.String(16))

    cvformat = db.relationship('Cvformat')
    employerformat = db.relationship('Employerformat')
