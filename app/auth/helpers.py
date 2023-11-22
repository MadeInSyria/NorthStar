from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class SignupForm (FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password_verification', message='Passwords must match'), Length(8, 32, message='Password must be between 8 and 32 characters')])
    password_verification = PasswordField('Password verification', validators=[DataRequired()])
    submit = SubmitField()

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 32, message='Password must be between 8 and 32 characters')])
    remember = BooleanField('Remember me')
    submit = SubmitField()