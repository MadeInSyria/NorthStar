from flask import render_template
from app.main import main
from app.extensions import db

@main.route('/')
def index():
    return render_template('main/index.html')