from flask import abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.component import component
from app.component.helpers import CreateComponentForm
from app.extensions import db
from app.models.components import Component
from app.models.drawers import Drawer


@login_required
@component.route('/<drawer_id>/')
def get_components_by_drawer(drawer_id):
    drawer = Drawer.query.get(drawer_id)
    
    if drawer == None:
        abort(404)
        
    components = Component.query.filter_by(drawer_id=drawer.id)
    
    return render_template('components/by_drawers.html', component=component)

@login_required
@component.route('<drawer_id>/create')
def create_component_form():
    form = CreateComponentForm()
    return render_template('component/create.html', form=form)

@login_required
@component.route('/create', methods=['POST'])
def create_cabinet():
    name = request.form.get('name')
    x = request.form.get('x')
    y = request.form.get('y')
    
    new_cabinet = Component(name=name, x=x, y=y, user_id=current_user.id)

    db.session.add(new_cabinet)
    db.session.commit()
    
    return redirect(url_for('cabinet.get_cabinets'))