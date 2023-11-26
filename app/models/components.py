from app.extensions import db

class Component(db.Model):
    
    __tablename__ = 'components'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    drawer_id = db.Column(db.Integer, db.ForeignKey('drawers.id'), nullable=False)
    drawer = db.relationship('Drawer', back_populates='components')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    