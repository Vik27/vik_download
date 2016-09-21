from app import db

class Chassis(db.Model):

    __tablename__ = "chassis"

    id = db.Column(db.Integer, primary_key = True)
    
    modelNo = db.Column(db.String(20))
    
    maxSlots = db.Column(db.Integer)
    
    connectionType = db.Column(db.Enum('USB', 'Ethernet'))

    devices = db.relationship('Devicetable', backref='chassis', lazy='dynamic')

    daqmxDeviceId = db.Column(db.String(128))
    
    def to_dict(self):
        return dict(
            modelNo = self.modelNo,
            maxSlots = self.maxSlots,
            connectionType = self.connectionType,
            daqmxDeviceId = self.daqmxDeviceId,
            id = self.id
        )

    def __repr__(self):
        return '<Chassis %r>' % (self.id)
