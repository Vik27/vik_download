from app import db

class Devicetable(db.Model):

    __tablename__ = "devicetable"
    
    id = db.Column(db.Integer, primary_key = True)

    firmwarename = db.Column(db.String(128), unique = True)
    
    businessId = db.Column(db.Integer,db.ForeignKey('business.id'))

    niChassisId = db.Column(db.Integer,db.ForeignKey('chassis.id'))

    queueId = db.Column(db.Integer, db.ForeignKey('queue.id'))

    hwsetups = db.relationship('HardwareSetup', backref='device', lazy='dynamic')

    def to_dict(self):
        return dict(
            firmwarename = self.firmwarename,
            businessId = self.businessId,
            niChassisId = self.niChassisId,
            queueId = self.queueId,
            id = self.id
        )

    def __repr__(self):
        return '<Devicetable %r>' % (self.id)