from flask import Blueprint

drawer = Blueprint('drawer', __name__, url_prefix="/drawers")

from app.drawer import routes