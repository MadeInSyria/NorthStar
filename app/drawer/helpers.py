from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired

class CreateDrawerForm (FlaskForm):
    x = IntegerField('X position in the cabinet', validators=[DataRequired()])
    y = IntegerField('Y position in the cabinet', validators=[DataRequired()])
    compartments = IntegerField('Number of compartments', validators=[DataRequired()])
    submit = SubmitField()
