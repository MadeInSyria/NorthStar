from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.drawer import drawer
from app.drawer.helpers import CreateDrawerForm
from app.extensions import db
from app.models.drawers import Drawer

@login_required
@drawer.route('/create')
def create_drawer_form():
    form = CreateDrawerForm()
    return render_template('drawer/create.html', form=form)

#@login_required
# @drawer.route('/create', methods=['POST'])
# def create_drawer_form():
#     x = request.form.get('x')
#     y = request.form.get('y')
    
#     new_drawer = Drawer(x=x, y=y, user_id=current_user.id)

#     db.session.add(new_drawer)
#     db.session.commit()
    
#     return redirect(url_for('drawer.get_drawers'))