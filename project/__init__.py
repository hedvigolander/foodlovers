from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from config import Config, DevelopmentConfig, StagingConfig, DevelopmentConfig
from flask.ext.heroku import Heroku
import os

app = Flask(__name__)


app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning




db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
csrf = CSRFProtect(app)
heroku = Heroku(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"
login_manager.session_protection = "strong"
login_manager.refresh_view = "users.login"


from project.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

@login_manager.unauthorized_handler
def unauthorized():
    return render_template('403.html')

# blueprints
from project.users.views import users_blueprint
from project.recipes.views import recipes_blueprint
from project.home.views import home_blueprint
from project.categories.views import categories_blueprint
from project.ingredients.views import ingredients_blueprint
# register the blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(recipes_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(categories_blueprint)
app.register_blueprint(ingredients_blueprint)

@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403
