from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class CreateCabinetForm (FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Email()])
    x = IntegerField('Height in units', validators=[DataRequired()])
    y = IntegerField('Width in units', validators=[DataRequired(), EqualTo('password_verification', message='Passwords must match'), Length(8, 32, message='Password must be between 8 and 32 characters')])
    submit = SubmitField()
