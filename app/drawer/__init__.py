from flask import Blueprint
from app.component import component

drawer = Blueprint('drawer', __name__, url_prefix="/drawers")

drawer.register_blueprint(component)

from app.drawer import routes