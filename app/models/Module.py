from app import db
from modquanmap import modquanmap

class Module(db.Model):

    __tablename__ = "module"
    
    id = db.Column(db.Integer, primary_key = True)
    
    modelNo = db.Column(db.String(20))
    
    maxChannels = db.Column(db.Integer)
    
    maxSamplingRate = db.Column(db.Integer)
    
    peakVoltRange = db.Column(db.Integer)
    
    type = db.Column(db.Enum('Analog_Input', 'Digital_Input', 'Digital_Output'))

    quantities = db.relationship('Quantity', secondary=modquanmap, backref=db.backref('moduless',lazy='dynamic'))
    
    hwchassmap = db.relationship('Hwchassismap', backref='module', lazy='dynamic')

    daqmxDeviceId = db.Column(db.String(128))
    # ADD PRODUCT ID (HEXADECIMAL)

    def to_dict(self):
        return dict(
            modelNo = self.modelNo,
            maxChannels = self.maxChannels,
            maxSamplingRate = self.maxSamplingRate,
            peakVoltRange = self.peakVoltRange,
            type = self.type,
            daqmxDeviceId = self.daqmxDeviceId,
            id = self.id,
            # quantities = self.quantities
        )

    def __repr__(self):
        return '<Module %r>' % (self.id)
