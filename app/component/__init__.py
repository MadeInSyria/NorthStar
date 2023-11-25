from flask import Blueprint

component = Blueprint('component', __name__, url_prefix="/components")

from app.component import routes