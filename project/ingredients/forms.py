from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.validators import DataRequired

#Form to add a ingredient and also a validator to see if the data is correct
class AddIngredientForm(FlaskForm):
    name = StringField('Ingredient name', validators=[DataRequired()])

#Form to edit a ingredient and also a validator to see if the data is correct
class EditIngredientForm(FlaskForm):
    name = StringField('Ingredient name', validators=[DataRequired()])
