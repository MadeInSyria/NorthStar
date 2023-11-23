from app.extensions import db

class Drawer(db.Model):
    
    __tablename__ = 'drawers'
    
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)
    cabinet_id = db.Column(db.Integer, db.ForeignKey('cabinets.id'), nullable=False)
    cabinet = db.relationship('Cabinet', back_populates='drawers')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    