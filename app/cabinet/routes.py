from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.cabinet import cabinet
from app.cabinet.helpers import CreateCabinetForm
from app.extensions import db
from app.models.cabinet import Cabinet


@login_required
@cabinet.route('/')
def get_cabinets():
    cabinets = current_user.cabinets
    return render_template('cabinet/all.html', cabinets=cabinets)

@login_required
@cabinet.route('/create')
def create_cabinet_form():
    form = CreateCabinetForm()
    return render_template('cabinet/create.html', form=form)

@login_required
@cabinet.route('/create', methods=['POST'])
def create_cabinet():
    name = request.form.get('name')
    x = request.form.get('x')
    y = True if request.form.get('y') else False
    
    new_cabinet = Cabinet(name=name, x=x, y=y, user_id=current_user.id)

    db.session.add(new_cabinet)
    db.session.commit()
    
    return redirect(url_for('cabinet.get_cabinets'))