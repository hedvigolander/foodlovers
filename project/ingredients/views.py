
from flask import render_template, Blueprint, request, redirect, url_for, flash, abort
from flask_login import login_user, current_user, login_required, logout_user, fresh_login_required
from project.models import Recipe, Category, Ingredient
from .forms import AddIngredientForm, EditIngredientForm
from project import db

ingredients_blueprint = Blueprint('ingredients', __name__)

#To show all the differents ingredients
@ingredients_blueprint.route('/ingredient')
@login_required
def index():
    ingredient = Ingredient.query.all()
    return render_template('ingredients.html', ingredients=ingredient)

#To add a ingredient through the form, if the form is valide through the validators then a new ingredientis created
@ingredients_blueprint.route('/ingredient/add', methods=['GET', 'POST'])
@fresh_login_required
def add():
    form = AddIngredientForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_ing = Ingredient(form.name.data)
            db.session.add(new_ing)
            db.session.commit()
            flash('New ingredient, {}, added!'.format(new_ing.name), 'success')
            return redirect(url_for('ingredients.index'))
        else:
            flash_errors(form)
            flash('ERROR! Ingredient was not added.', 'error')

    return render_template('add_ingredient.html',form=form)

#To edit a given ingredient through the form as an admin, if the form is valide through the validators then the ingredient is changed
@ingredients_blueprint.route('/ingredient/edit/<ingredient_id>', methods=['GET', 'POST'])
@fresh_login_required
def admin_edit_ingredient(ingredient_id):
    ingredient = Ingredient.query.filter_by(id=ingredient_id).first_or_404()
    if current_user.role=='admin':

        form = EditIngredientForm(request.form)

        if request.method == 'POST':
            if form.validate_on_submit():
                update_counter = 0

                if form.name.data is not None and form.name.data != ingredient.name:
                    flash('DEBUG: Updating ingredient.name to {}.'.format(form.name.data), 'debug')
                    update_counter += 1
                    ingredient.name = form.name.data

                if update_counter > 0:
                    db.session.add(ingredient)
                    db.session.commit()

                    flash('Ingredient has been updated for {}.'.format(ingredient.name), 'success')
                else:
                    flash('No updates made to the ingredient ({}). Please update at least one field.'.format(ingredient.name), 'error')

                return redirect(url_for('ingredients.index'))
            else:
                flash_errors(form)
                flash('ERROR! Ingredient was not edited.', 'error')

        return render_template('edit_ingredient.html', form=form, ingredient=ingredient)
    return render_template('403.html')
