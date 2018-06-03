from flask import render_template, Blueprint, request, redirect, url_for, flash

home_blueprint = Blueprint('home', __name__)

#The first site
@home_blueprint.route('/')
@home_blueprint.route('/index')
def index():
    return render_template('index.html')
