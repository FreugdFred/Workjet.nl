from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, IntegerField, SelectField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo



class EmailForm(FlaskForm):
    email = EmailField('email', [Email(), InputRequired(), Length(min=5, max=35)])
    

class BlogForm(FlaskForm):
    post_title = TextAreaField('title',[Length(min=1, max=400)])
    post_text = TextAreaField('text',[Length(min=1, max=5000)])
    post_creator = TextAreaField('creator',[Length(min=1, max=100)])
    
    
class PasswordForm(FlaskForm):
    password = PasswordField('password', [InputRequired(), Length(min=10, max=35), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')
    employer = SelectField('employer', choices=[('None', ' '), ('employer', 'werkgever'), ('employee', 'werknemer')])
    
    
class ResetpasswordForm(FlaskForm):
    password = PasswordField('password', [InputRequired(), Length(min=10, max=35), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')


class Loginform(FlaskForm):
    email = EmailField('email', [Email(), InputRequired(), Length(min=5, max=35)])
    password = PasswordField('password', [InputRequired(), Length(min=10, max=35)])
    
    
class Cvform(FlaskForm):
    name = StringField('name', [InputRequired(), Length(min=1, max=100)])
    age = IntegerField('age', [InputRequired()])
    language = StringField('language', [InputRequired(), Length(min=2, max=700)])
    region = SelectField('region', choices=[("'s Hertogenbosch"), ("Alkmaar"), ("Almelo"), ("Almere"), ("Alphen aan den Rijn"), ("Amersfoort"), ("Amstelveen"), ("Amsterdam"), ("Apeldoorn"), ("Arnhem"), ("Assen"), ("Bergen op Zoom"), ("Breda"), ("Capelle aan den IJssel"), ("Delft"), ("Den Haag"), ("Den Helder"), ("Deventer"), ("Doetinchem"), ("Dordrecht"), ("Ede"), ("Eindhoven"), ("Eindhoven"), ("Emmen"), ("Enschede"), ("Flevoland"), ("Gouda"), ("Haarlem"), ("Haarlemmermeer"), ("Heerlen"), ("Helmond"), ("Hengelo"), ("Hilversum"), ("Hoogeveen"), ("Hoorn"), ("Katwijk"), ("Leeuwarden"), ("Leiden"), ("Leidschendam-Voorburg"), ("Lelystad"), ("Maastricht"), ("Middelburg"), ("Nieuwegein"), ("Nijmegen"), ("Oss"), ("Purmerend"), ("Roermond"), ("Roosendaal"), ("Rotterdam"), ("Schiedam"), ("Sittard-Geleen"), ("Spijkenisse"), ("Súdwest-Fryslân"), ("Terneuzen"), ("Tilburg"), ("Utrecht"), ("Veenendaal"), ("Venlo"), ("Vlaardingen"), ("Westland"), ("Zaanstad"), ("Zeist"), ("Zoetermeer"), ("Zwolle")])
    fulltime = SelectField('fulltime', choices=[('Full-time', 'deeltijd'), ('Part-time', 'voltijd')])
    schooling = TextAreaField('schooling', [InputRequired(), Length(min=2, max=100)])
    men = SelectField('men', choices=[('Men', 'man'), ('Lady', 'vrouw')])
    comment = TextAreaField('comment', [InputRequired(), Length(min=2, max=700)])
    contact = TextAreaField('contact', [InputRequired(), Length(min=2, max=100)])
    
    outexperience = TextAreaField('outexperience', [InputRequired(), Length(min=2, max=500)])
    inexperience = TextAreaField('inexperience', [InputRequired(), Length(min=2, max=500)])
    currentlylooking = SelectField('currentlylooking', choices=[('Yes', 'ja'), ('No', 'nee')])
    
    landbouw = BooleanField()
    bouw = BooleanField()
    handel = BooleanField()
    gezondheidszorg = BooleanField()
    communicatie = BooleanField()
    onderwijs = BooleanField()
    horeca = BooleanField()
    transport = BooleanField()
    productie = BooleanField()
    engineering = BooleanField()
    
    
class Amdinform(FlaskForm):
    userid = TextAreaField('userid', [InputRequired(), Length(min=1, max=100)])
    email = EmailField('email', [Email(), InputRequired(), Length(min=5, max=35)])
    password = TextAreaField('password', [InputRequired(), Length(min=1, max=300)])
    creationdate = TextAreaField('creationdate', [InputRequired(), Length(min=1, max=150)])
    lastlogin = TextAreaField('lastlogin', [InputRequired(), Length(min=1, max=150)])
    employer = SelectField('employer', choices=[('employer', 'werkgever'), ('employee', 'werknemer')])
    ip = TextAreaField('ip', [InputRequired(), Length(min=1, max=30)])
    
    
class Adminemployer(FlaskForm):
    coins = TextAreaField('coins', [InputRequired(), Length(min=1, max=30000)])
    subscription = TextAreaField('subscription', [InputRequired(), Length(min=1, max=4)])
    user_id = TextAreaField('user_id', [InputRequired(), Length(min=1, max=30000)])

 
class Adminemployee(FlaskForm):
    name = StringField('name', [Length(min=1, max=100)])
    age = IntegerField('age')
    language = StringField('language', [Length(min=2, max=700)])
    region = SelectField('region', choices=[("'s Hertogenbosch"), ("Alkmaar"), ("Almelo"), ("Almere"), ("Alphen aan den Rijn"), ("Amersfoort"), ("Amstelveen"), ("Amsterdam"), ("Apeldoorn"), ("Arnhem"), ("Assen"), ("Bergen op Zoom"), ("Breda"), ("Capelle aan den IJssel"), ("Delft"), ("Den Haag"), ("Den Helder"), ("Deventer"), ("Doetinchem"), ("Dordrecht"), ("Ede"), ("Eindhoven"), ("Eindhoven"), ("Emmen"), ("Enschede"), ("Flevoland"), ("Gouda"), ("Haarlem"), ("Haarlemmermeer"), ("Heerlen"), ("Helmond"), ("Hengelo"), ("Hilversum"), ("Hoogeveen"), ("Hoorn"), ("Katwijk"), ("Leeuwarden"), ("Leiden"), ("Leidschendam-Voorburg"), ("Lelystad"), ("Maastricht"), ("Middelburg"), ("Nieuwegein"), ("Nijmegen"), ("Oss"), ("Purmerend"), ("Roermond"), ("Roosendaal"), ("Rotterdam"), ("Schiedam"), ("Sittard-Geleen"), ("Spijkenisse"), ("Súdwest-Fryslân"), ("Terneuzen"), ("Tilburg"), ("Utrecht"), ("Veenendaal"), ("Venlo"), ("Vlaardingen"), ("Westland"), ("Zaanstad"), ("Zeist"), ("Zoetermeer"), ("Zwolle")])
    fulltime = SelectField('fulltime', choices=[('Full-time', 'deeltijd'), ('Part-time', 'voltijd')])
    schooling = TextAreaField('schooling', [ Length(min=2, max=100)])
    men = SelectField('men', choices=[('Men', 'man'), ('Lady', 'vrouw')])
    comment = TextAreaField('comment', [Length(min=2, max=700)])
    contact = TextAreaField('contact', [Length(min=2, max=100)])
    
    outexperience = TextAreaField('outexperience', [Length(min=2, max=500)])
    inexperience = TextAreaField('inexperience', [Length(min=2, max=500)])
    currentlylooking = SelectField('currentlylooking', choices=[('Yes', 'ja'), ('No', 'nee')])
    
    landbouw = BooleanField()
    bouw = BooleanField()
    handel = BooleanField()
    gezondheidszorg = BooleanField()
    communicatie = BooleanField()
    onderwijs = BooleanField()
    horeca = BooleanField()
    transport = BooleanField()
    productie = BooleanField()
    engineering = BooleanField()
    

