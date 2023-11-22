from flask import Blueprint

cabinet = Blueprint('cabinet', __name__, url_prefix="/cabinets")

from app.cabinet import routes