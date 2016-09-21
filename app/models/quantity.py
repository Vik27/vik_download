from app import db
from modquanmap import modquanmap


class Quantity(db.Model):

    __tablename__ = "quantity"

    id = db.Column(db.Integer, primary_key = True)
    
    name = db.Column(db.String(30))
    
    modules = db.relationship('Module', secondary=modquanmap, backref=db.backref('quants',lazy='dynamic'))
    
    unitId=db.relationship('Unit', backref='quantity',lazy='dynamic')

    def to_dict(self):
        return dict(
            name = self.name,
            id = self.id
        )

    def __repr__(self):
        return '<Quantity %r>' % (self.id)
