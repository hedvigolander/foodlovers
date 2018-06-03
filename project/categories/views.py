
from flask import render_template, Blueprint, request, redirect, url_for, flash

from sqlalchemy.exc import IntegrityError
from project import db, mail, app
from threading import Thread
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime
from flask_login import login_user, current_user, login_required, logout_user
from project.models import Recipe, Category

categories_blueprint = Blueprint('categories', __name__)

#To show all the start site of all the different categories
@categories_blueprint.route('/category')
@login_required
def category():
    return render_template('category.html')

#To show all the recipes of a certain category
@categories_blueprint.route('/category/breakfast')
@login_required
def breakfast():
    breakfast = Recipe.query.filter_by(category_id=1)
    category = Category.query.filter_by(id=1)
    return render_template('categories_sites.html', category= category, recipes=breakfast)

@categories_blueprint.route('/category/dinner')
@login_required
def dinner():
    dinner = Recipe.query.filter_by(category_id=2)
    category = Category.query.filter_by(id=2)
    return render_template('categories_sites.html', category= category, recipes=dinner)

@categories_blueprint.route('/category/baking')
@login_required
def baking():
    baking = Recipe.query.filter_by(category_id=3)
    category = Category.query.filter_by(id=3)
    return render_template('categories_sites.html', category= category,recipes=baking)

@categories_blueprint.route('/category/summer')
@login_required
def summer():
    summer = Recipe.query.filter_by(category_id=4)
    category = Category.query.filter_by(id=4)
    return render_template('categories_sites.html',category= category, recipes=summer)

@categories_blueprint.route('/category/winter')
@login_required
def winter():
    winter = Recipe.query.filter_by(category_id=5)
    category = Category.query.filter_by(id=5)
    return render_template('categories_sites.html', category= category,recipes=winter)
