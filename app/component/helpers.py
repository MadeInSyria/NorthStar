import requests

from flask import abort, flash, redirect, url_for
from flask_login import current_user
from flask_wtf import FlaskForm
from sqlalchemy import cast, String
from wtforms import IntegerField, HiddenField, SelectMultipleField, StringField, SubmitField
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

class ClearLEDForm (FlaskForm):
    submit = SubmitField('Clear all LEDs')

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

def turn_cabinet_led_on(checkout_list):
    for cabinet, drawers in checkout_list.items():
        host = cabinet.host
        for drawer in drawers:
            led_number = compute_led_number(drawer.x, drawer.y, cabinet.x)
            requests.post(f'http://{host}/led_on', data={'led_list': led_number})
            

def turn_cabinet_led_off():
    for cabinet in current_user.cabinets:
        requests.get(f'http://{cabinet.host}/all_led_off')
            
            
            
def compute_led_number(drawer_x, drawer_y, cabinet_x):
    if drawer_y % 2 == 0:
        led_number = cabinet_x * drawer_y - drawer_x 
    else:
        led_number = (drawer_x + (drawer_y -1) * cabinet_x) - 1
        
    return led_number