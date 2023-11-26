from flask import abort, flash, redirect, url_for
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired

from app.models.components import Component

class CreateComponentForm (FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', default=-1)
    submit = SubmitField()
    
class UpdateComponentForm (FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity')
    submit = SubmitField()
    
def component_ownership_validation(component_id):
    component = Component.query.get(component_id)
    
    if component == None:
        abort(404)
        
    drawer = component.drawer
    
    if drawer.cabinet.user.id != current_user.id:
        flash('This cabinet is not owned by the user.')
        return redirect(url_for('cabinet.drawer.get_drawer', drawer_id=drawer.id))
    
    return component