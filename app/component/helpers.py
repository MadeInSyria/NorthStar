from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired

class CreateComponentForm (FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    quantity = IntegerField('Password verification', validators=[DataRequired()])
    submit = SubmitField()