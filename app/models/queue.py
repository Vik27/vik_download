from app import db

class Queue(db.Model):

    __tablename__ = "queue"
    
    id = db.Column(db.Integer, primary_key = True)

    queuename = db.Column(db.String(128), unique = True)
    
    businessId = db.Column(db.Integer,db.ForeignKey('business.id'))

    devices = db.relationship('Devicetable', backref='queue', lazy='dynamic')

    def to_dict(self):
        return dict(
            queuename = self.queuename,
            businessId = self.businessId,
            id = self.id
        )

    def __repr__(self):
        return '<Queue %r>' % (self.id)