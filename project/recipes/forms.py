
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, TextAreaField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired

#The form to add a recipe who also have validators for each field
class AddRecipeForm(FlaskForm):


    recipe_title = StringField('Recipe Title', validators=[DataRequired()])
    recipe_description = TextAreaField('Recipe Description', validators=[DataRequired()])
    recipe_instruction = TextAreaField('Recipe Instruction', validators=[DataRequired()])
    category_id = RadioField('Category', validators=[DataRequired()], choices=[("Breakfast", 'Breakfast'),("Dinner", 'Dinner'),("Baking", 'Baking/Snacks'),("Summer", 'Summer'),("Winter", 'Winter')])
    ingredient_id= SelectMultipleField('Ingredients',validators=[DataRequired()], choices=[])



#The form to edit a recipe who also have validators for each field
class EditRecipeForm(FlaskForm):
    recipe_title = StringField('Recipe Title', validators=[DataRequired()])
    recipe_description = TextAreaField('Short Recipe Description', validators=[DataRequired()])
    recipe_instruction = TextAreaField('Recipe Instruction', validators=[DataRequired()])
    category_id = RadioField('Category', validators=[DataRequired()], choices=[("Breakfast", 'Breakfast'),("Dinner", 'Dinner'),("Baking", 'Baking/Snacks'),("Summer", 'Summer'),("Winter", 'Winter')])
    ingredient_id= SelectMultipleField('Ingredients',validators=[DataRequired()], choices=[])
