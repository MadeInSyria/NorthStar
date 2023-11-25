from flask import abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.drawer import drawer
from app.drawer.helpers import CreateDrawerForm
from app.extensions import db
from app.models.cabinets import Cabinet
from app.models.drawers import Drawer

@login_required
@drawer.route('<cabinet_id>/create')
def create_drawer_form(cabinet_id):
    form = CreateDrawerForm()
    return render_template('drawer/create.html', form=form)

@login_required
@drawer.route('<cabinet_id>/create', methods=['POST'])
def create_drawer(cabinet_id):
    
    cabinet = Cabinet.query.get(cabinet_id)
    
    x = request.form.get('x')
    y = request.form.get('y')
    
    drawer = Drawer.query.filter_by(cabinet_id=cabinet_id, x=x, y=y).first()
    
    print(drawer)
    
    if drawer != None:
        abort(409)
    
    if cabinet == None:
        abort(404)
    
    if cabinet.user.id != current_user.id:
        abort(403)
    
    new_drawer = Drawer(x=x, y=y, cabinet_id=cabinet_id)

    db.session.add(new_drawer)
    db.session.commit()
    
    return redirect(url_for('cabinet.get_cabinet', cabinet_id=cabinet_id))