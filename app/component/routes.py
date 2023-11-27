import requests

from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.component import component
from app.component.helpers import ClearLEDForm, CheckoutComponentForm, CreateComponentForm, UpdateComponentForm, component_ownership_validation, turn_cabinet_led_on, turn_cabinet_led_off
from app.extensions import db
from app.models.cabinets import Cabinet
from app.models.components import Component
from app.models.drawers import Drawer


@login_required
@component.route('/checkout')
def checkout_component_form():
    form = CheckoutComponentForm()
    
    return render_template('component/checkout_form.html', form=form)

@login_required
@component.route('/checkout', methods=['POST'])
def checkout_component():
    components = request.form.getlist('components')
    checkout_list = dict()
    
    for c in components:
        component = Component.query.get(c)
        drawer = component.drawer
        cabinet = drawer.cabinet
        
        if cabinet not in checkout_list:
            checkout_list[cabinet] = dict()
        
        if drawer not in checkout_list[cabinet]:
            checkout_list[cabinet][drawer] = []
        
        checkout_list[cabinet][drawer].append(component)
    
    turn_cabinet_led_on(checkout_list)
    form = ClearLEDForm()
    return render_template('component/checkout.html', checkout_list=checkout_list, form=form)

@login_required
@component.route('/clear_led', methods=['POST'])
def clear_led():
    turn_cabinet_led_off()
    return redirect(url_for('cabinet.get_cabinets'))

@login_required
@component.route('<drawer_id>/create')
def create_component_form(drawer_id):
    form = CreateComponentForm()
    
    return render_template('component/create.html', form=form)

@login_required
@component.route('<drawer_id>/create', methods=['POST'])
def create_component(drawer_id):
    name = request.form.get('name')
    quantity = request.form.get('quantity')
    
    drawer = Drawer.query.get(drawer_id)
    
    if drawer == None:
        flash('This drawer does not exist.')
        return redirect(url_for('cabinet.drawer.get_drawer', drawer_id=drawer_id))
    
    if drawer.cabinet.user.id != current_user.id:
        flash('This cabinet is not owned by the user.')
        return redirect(url_for('cabinet.drawer.get_drawer', drawer_id=drawer_id))
    
    if drawer.compartments <= len(drawer.components):
        flash('This drawer is already full.')
        return redirect(url_for('cabinet.drawer.get_drawer', drawer_id=drawer_id))
        
    new_component = Component(name=name, quantity=quantity, drawer_id=drawer_id)

    db.session.add(new_component)
    db.session.commit()
    
    return redirect(url_for('cabinet.drawer.get_drawer', drawer_id=drawer_id))

@login_required
@component.route('<component_id>')
def delete_component(component_id):
    component = component_ownership_validation(component_id)
    
    db.session.delete(Component.query.get(component_id))
    db.session.commit()
    
    return redirect(url_for('cabinet.drawer.get_drawer', drawer_id=component.drawer.id))

@login_required
@component.route('<drawer_id>/update/<component_id>')
def update_component_form(component_id, drawer_id):
    component = component_ownership_validation(component_id)
    
    form = UpdateComponentForm(obj=component)
    return render_template('component/create.html', form=form)

@login_required
@component.route('<drawer_id>/update/<component_id>', methods=['POST'])
def update_component(component_id, drawer_id):
    component = component_ownership_validation(component_id)
    
    component.name = request.form.get('name')
    component.quantity = request.form.get('quantity')
    db.session.commit()
    
    return redirect(url_for('cabinet.drawer.get_drawer', drawer_id=drawer_id))