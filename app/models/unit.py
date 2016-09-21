from app import db

class Unit(db.Model):

    __tablename__ = "unit"

    id = db.Column(db.Integer, primary_key = True)
    
    name = db.Column(db.String(30))
    
    quantityID = db.Column(db.Integer,db.ForeignKey('quantity.id'))
    
    channels=db.relationship('Channelsetup', backref='unit', lazy='dynamic')


    def to_dict(self):
        return dict(
            name = self.name,
            id = self.id,
            quantityID = self.quantityID
        )

    def __repr__(self):
        return '<Unit %r>' % (self.id)
