from app import db
# from channelnumbertemplate import channelnumbertemplate

class Hwchaschanmap(db.Model):

    __tablename__ = "hwchaschanmap"

    id = db.Column(db.Integer, primary_key = True)
    
    name = db.Column(db.String(32))
    
    channelnumber = db.Column(db.Integer)
    
    # trigger = db.relationship('HardwareSetup', backref='hwchaschan', lazy='dynamic')
    # trigger relationship for digital channels in hardwaresetup
    
    channelTemplateId = db.Column(db.Integer,db.ForeignKey('channelsetup.id'))
    
    hwchassId = db.Column(db.Integer,db.ForeignKey('hwchassismap.id'))

    peakvalue = db.Column(db.Float)
    
    #rawdatas = db.relationship('Rawdata', backref='hwchaschanmap', lazy='dynamic')

    def to_dict(self):
        return dict(
            name = self.name,
            channelnumber = self.channelnumber,
            # trigger = self.trigger,
            channelTemplateId = self.channelTemplateId,
            hwchassId = self.hwchassId,
            peakvalue = self.peakvalue,
            id = self.id
        )

    def __repr__(self):
        return '<Hwchaschanmap %r>' % (self.id)
