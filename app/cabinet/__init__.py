from flask import Blueprint

from app.drawer import drawer

cabinet = Blueprint('cabinet', __name__, url_prefix="/cabinets")

cabinet.register_blueprint(drawer)

from app.cabinet import routes