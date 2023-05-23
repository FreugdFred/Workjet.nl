from flask import Flask
from datetime import timedelta
from itsdangerous import URLSafeTimedSerializer
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from os import path
import detectlanguage


db = SQLAlchemy()
DB_NAME = "database.db"


app = Flask(__name__)
app.config['SECRET_KEY'] = "MY ONDERBROKENLOOPT HOOF"
app.permanent_session_lifetime = timedelta(minutes=20)
save_url_token = URLSafeTimedSerializer(app.config['SECRET_KEY'])
detectlanguage.configuration.api_key = "97f69489dd925a3a8696ffd47db01cb1"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)


from .Errorpage import errorpage_blueprint
from .Admin import admin_blueprint
from .Admin import adminedit_blueprint
from .Admin import admindelete_blueprint
from .Blog import blog_blueprint
from .Blog import bloglike_blueprint
from .Blog import blogget_blueprint
from .Blog import blogadminpost_blueprint
from .Blog import blogadmindelete_blueprint
from .Contact import contact_blueprint
from .Faq import faq_blueprint
from .Forgotpassword import forgotpassword_blueprint
from .Forgotpassword import forgotpassword_token_blueprint
from .Home import home_blueprint
from .Login import login_blueprint
from .Login import logout_blueprint
from .Profile import profile_blueprint
from .Register import register_blueprint
from .Registertoken import register_token_blueprint
from .Saved import saved_blueprint
from .Saved import savedask_blueprint
from .Search import search_blueprint
from .Search import searchask_blueprint
from .Werkgever import werkgever_blueprint
from .Werknemer import werknemer_blueprint


app.register_blueprint(errorpage_blueprint, url_prefix="/")
app.register_blueprint(admin_blueprint, url_prefix="/")
app.register_blueprint(adminedit_blueprint, url_prefix='/', name="/adminedit")
app.register_blueprint(admindelete_blueprint, url_prefix='/', name="/admindelete")
app.register_blueprint(blog_blueprint, url_prefix='/', name="blog")
app.register_blueprint(blogget_blueprint, url_prefix='/', name="blogget")
app.register_blueprint(bloglike_blueprint, url_prefix='/', name="bloglike")
app.register_blueprint(blogadminpost_blueprint, url_prefix='/', name="blogpostadmin")
app.register_blueprint(blogadmindelete_blueprint, url_prefix='/', name="blogdeleteadmin")
app.register_blueprint(contact_blueprint, url_prefix="/")
app.register_blueprint(faq_blueprint, url_prefix="/")
app.register_blueprint(forgotpassword_blueprint, url_prefix="/")
app.register_blueprint(forgotpassword_token_blueprint, url_prefix="/", name="forgotpasswordtoken")
app.register_blueprint(home_blueprint, url_prefix="/")
app.register_blueprint(login_blueprint, url_prefix="/")
app.register_blueprint(logout_blueprint, url_prefix="/", name="logout")
app.register_blueprint(profile_blueprint, url_prefix="/")
app.register_blueprint(register_blueprint, url_prefix="/")
app.register_blueprint(register_token_blueprint, url_prefix="/")
app.register_blueprint(saved_blueprint, url_prefix="/")
app.register_blueprint(savedask_blueprint, url_prefix="/", name="savedask")
app.register_blueprint(search_blueprint, url_prefix="/")
app.register_blueprint(searchask_blueprint, url_prefix="/", name="searchask")
app.register_blueprint(werkgever_blueprint, url_prefix="/")
app.register_blueprint(werknemer_blueprint, url_prefix="/")

login_manager = LoginManager()
login_manager.login_view = 'Login.login'
login_manager.init_app(app)

from website.Models import User

if not path.exists(f'website/{DB_NAME}'):
    db.create_all(app=app)
    print('Created Database!')


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


    



