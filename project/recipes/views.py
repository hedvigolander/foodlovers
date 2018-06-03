from flask import render_template, Blueprint, request, redirect, url_for, flash
from project.models import Recipe, User, Ingredient, Index
from flask_login import login_user, current_user, login_required, logout_user, fresh_login_required
from .forms import AddRecipeForm, EditRecipeForm
from project import db
from datetime import datetime

recipes_blueprint = Blueprint('recipes', __name__)

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'info')

#To show all recipes and also the user who have created them
@recipes_blueprint.route('/recipes')
@login_required
def recipes():
    all_recipes = Recipe.query.all()
    user = User.query.all()
    return render_template('recipes.html', recipes=all_recipes, users=user)

#To show all the current user's recipes
#The recipes are filtered by the id of the current user
@recipes_blueprint.route('/user/recipes')
@login_required
def user_recipes():
    all_user_recipes = Recipe.query.filter_by(user_id=current_user.id)
    return render_template('user_recipes.html', user_recipes=all_user_recipes)

#To modify a given recipe in parameter, the different choices for ingredients are created dynamically
#if something is modified and correctly then the recipe is committed
@recipes_blueprint.route('/recipes/details/<recipe_id>', methods=['GET', 'POST'])
@fresh_login_required
def recipes_details(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()
    user = User.query.all()

    index = Index.query.filter_by(recipe_id=recipe_id)

    ingredients= Ingredient.query.all()

    return render_template('recipes_detail.html', users=user, recipe=recipe, index=index, ingredients=ingredients )

#To add a recipe, the different choices for ingredients are created dynamically
#the category returns a name which then are transformed into a id
@recipes_blueprint.route('/recipes/add', methods=['GET', 'POST'])
@fresh_login_required
def add_recipe():
    ingredients = [(c.name, c.name) for c in Ingredient.query.all()]
    form = AddRecipeForm(request.form)
    form.ingredient_id.choices = ingredients


    if request.method == 'POST':
        if form.validate_on_submit():

            if form.category_id.data =="Breakfast":
                id=1
            elif form.category_id.data =="Dinner":
                id=2
            elif form.category_id.data =="Baking":
                id=3
            elif form.category_id.data =="Summer":
                id=4
            elif form.category_id.data =="Winter":
                id=5

            new_recipe = Recipe(form.recipe_title.data, form.recipe_description.data, form.recipe_instruction.data, current_user.id, id)
            db.session.add(new_recipe)
            db.session.commit()

            for i in form.ingredient_id.data:
                for j in Ingredient.query.all():
                    if(i==j.name):
                        index=Index(j.id, new_recipe.id)
                        db.session.add(index)
                        db.session.commit()

            flash('New recipe, {}, added!'.format(new_recipe.recipe_title), 'success')
            return redirect(url_for('recipes.recipes'))
        else:
            flash_errors(form)
            flash('ERROR! Recipe was not added.', 'error')

    return render_template('add_recipe.html',form=form)

#To delete a given recipe in parameter
@recipes_blueprint.route('/user/recipes/delete/<recipe_id>')
@fresh_login_required
def delete_recipe(recipe_id):

    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()
    if current_user.id==recipe.user_id:


        db.session.delete(recipe)
        db.session.commit()

        for i in Index.query.filter_by(recipe_id=recipe_id):
            db.session.delete(i)
            db.session.commit()

        flash('{} was deleted.'.format(recipe.recipe_title), 'success')
        return redirect(url_for('recipes.user_recipes'))

    return render_template('403.html')

#To modify a given recipe in parameter, the different choices for ingredients are created dynamically
#if something is modified and correctly then the recipe is committed
@recipes_blueprint.route('/user/recipes/edit/<recipe_id>', methods=['GET', 'POST'])
@fresh_login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()
    if current_user.id==recipe.user_id:

        for i in Index.query.filter_by(recipe_id=recipe_id):
            db.session.delete(i)
            db.session.commit()

        ingredients = [(c.name, c.name) for c in Ingredient.query.all()]
        form = EditRecipeForm(request.form)
        form.ingredient_id.choices = ingredients



        if request.method == 'POST':
            if form.validate_on_submit():
                update_counter = 0

                if form.recipe_title.data is not None and form.recipe_title.data != recipe.recipe_title:
                    flash('DEBUG: Updating recipe.recipe_title to {}.'.format(form.recipe_title.data), 'debug')
                    update_counter += 1
                    recipe.recipe_title = form.recipe_title.data

                if form.recipe_description.data is not None and form.recipe_description.data != recipe.recipe_description:
                    flash('DEBUG: Updating recipe.recipe_description to {}.'.format(form.recipe_description.data), 'debug')
                    update_counter += 1
                    recipe.recipe_description = form.recipe_description.data

                if form.recipe_instruction.data is not None and form.recipe_instruction.data != recipe.recipe_instruction:
                    flash('DEBUG: Updating recipe.recipe_description to {}.'.format(form.recipe_instruction.data), 'debug')
                    update_counter += 1
                    recipe.recipe_instruction = form.recipe_instruction.data

                if form.category_id.data is not None and form.category_id.data != recipe.category_id:
                    flash('DEBUG: Updating recipe.category_id to {}.'.format(form.category_id.data), 'debug')
                    update_counter += 1


                    if form.category_id.data =="Breakfast":
                        id=1
                    elif form.category_id.data =="Dinner":
                        id=2
                    elif form.category_id.data =="Baking":
                        id=3
                    elif form.category_id.data =="Summer":
                        id=4
                    elif form.category_id.data =="Winter":
                        id=5
                    recipe.category_id = id

                if update_counter > 0:
                    db.session.add(recipe)
                    db.session.commit()

                    for i in form.ingredient_id.data:
                        for j in Ingredient.query.all():
                            if(i==j.name):
                                index=Index(j.id, recipe.id)
                                db.session.add(index)
                                db.session.commit()

                    flash('Recipe has been updated for {}.'.format(recipe.recipe_title), 'success')
                else:
                    flash('No updates made to the recipe ({}). Please update at least one field.'.format(recipe.recipe_title), 'error')

                return redirect(url_for('recipes.user_recipes'))
            else:
                flash_errors(form)
                flash('ERROR! Recipe was not edited.', 'error')

        return render_template('edit_recipe.html', form=form, recipe=recipe)
    return render_template('403.html')
