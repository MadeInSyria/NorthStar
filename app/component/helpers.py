from flask import abort, flash, redirect, url_for
from flask_login import current_user
from flask_wtf import FlaskForm
from sqlalchemy import cast, String
from wtforms import IntegerField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import DataRequired

from app.extensions import db
from app.models.cabinets import Cabinet
from app.models.components import Component
from app.models.drawers import Drawer


class CheckoutComponentForm (FlaskForm):
    components = SelectMultipleField('Component Name', validators=[DataRequired()], coerce=int)
    submit = SubmitField()
    
    def __init__(self):
        super(CheckoutComponentForm, self).__init__()
        cabinets_id = db.select(Cabinet.id).filter_by(user_id=current_user.id)
        drawers_id = db.select(Drawer.id).where(Drawer.cabinet_id.in_(cabinets_id))
        components = Component.query.where(Component.drawer_id.in_(drawers_id))
        
        choices = [(component.id, component.name) for component in components] 
        self.components.choices = choices

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