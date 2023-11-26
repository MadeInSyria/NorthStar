from app.extensions import db
from app.models.components import Component

class Drawer(db.Model):
    
    __tablename__ = 'drawers'
    
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)
    compartments = db.Column(db.Integer, nullable=False, default=1)
    cabinet_id = db.Column(db.Integer, db.ForeignKey('cabinets.id'), nullable=False)
    cabinet = db.relationship('Cabinet', back_populates='drawers')
    components = db.relationship('Component', back_populates='drawer')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    