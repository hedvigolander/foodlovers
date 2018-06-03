from project import db, bcrypt
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import event, DDL


class Recipe(db.Model):

    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    recipe_title = db.Column(db.String, nullable=False)
    recipe_description = db.Column(db.String, nullable=False)
    recipe_instruction = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    index = db.relationship('Index', backref='recipe', lazy='dynamic')
    created_on = db.Column(db.Date, nullable=True)
    modified_on = db.Column(db.Date, nullable=True)

    def __init__(self, title,  description, instruction, user_id, category_id):
        self.recipe_title = title
        self.recipe_description = description
        self.recipe_instruction = instruction
        self.user_id = user_id
        self.category_id=category_id

    def __repr__(self):
        return '<title {}'.format(self.name)




class Category(db.Model):

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    recipes = db.relationship('Recipe', backref='category', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<title {}'.format(self.name)

class Ingredient(db.Model):

    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    index = db.relationship('Index', backref='ingredient', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<title {}'.format(self.name)

class Index(db.Model):

    __tablename__ = "index"

    id = db.Column(db.Integer, primary_key=True)
    ing_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))

    def __init__(self, ing_id, recipe_id ):
        self.ing_id=ing_id
        self.recipe_id=recipe_id

    def __repr__(self):
        return '<title {}'.format(self.name)


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    email_confirmation_sent_on = db.Column(db.DateTime, nullable=True)
    email_confirmed = db.Column(db.Boolean, nullable=True, default=False)
    email_confirmed_on = db.Column(db.DateTime, nullable=True)
    role = db.Column(db.String, default='user')
    recipes = db.relationship('Recipe', backref='user', lazy='dynamic')




    def __init__(self, username, email, password, role):

        self.username=username
        self.email = email
        self.password=password
        self.authenticated = False
        self.email_confirmation_sent_on = None
        self.email_confirmed = False
        self.email_confirmed_on = None
        self.role=role


    def is_correct_password(self, passwordcheck):
        return check_password_hash(self.password, passwordcheck)

    def is_confirmed(self):
        return self.email_confirmed

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        """Requires use of Python 3"""
        return str(self.id)

    def __repr__(self):
        return '<User {0}>'.format(self.name)
