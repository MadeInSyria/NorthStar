from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired


class CreateCabinetForm (FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    host = StringField('Host/IP', validators=[DataRequired()])
    x = IntegerField('Height in units', validators=[DataRequired()])
    y = IntegerField('Width in units', validators=[DataRequired()])
    submit = SubmitField()


def generate_drawer_map(drawers):
    drawer_map = [[]]
    for drawer in drawers:
        drawer_map.append((drawer.x, drawer.y))
        drawer_map[0].append(drawer.id)
        
    return drawer_map