from flask import redirect, render_template, url_for
from flask_login import current_user

from app.main import main
from app.extensions import db


@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for("cabinet.get_cabinets"))
    else:
        return render_template('main/index.html')