from app import db

class Hwchassismap(db.Model):
    
    __tablename__ = "hwchassismap"

    id = db.Column(db.Integer, primary_key = True)
    
    slotnumber = db.Column(db.Integer)
    
    moduleID = db.Column(db.Integer,db.ForeignKey('module.id'))
    
    hwSetupID = db.Column(db.Integer,db.ForeignKey('hardwaresetup.id'))

    hwchaschanmaps = db.relationship('Hwchaschanmap', backref='hwchaschanmap', lazy='dynamic')

    samplingrate = db.Column(db.Integer)
    # ADD SAMPLING RATE FOR EACH ROW. I,E, EACH MODULE
    

    def to_dict(self):
        return dict(
            slotnumber = self.slotnumber,
            id = self.id,
            moduleID=self.moduleID,
            hwSetupID=self.hwSetupID,
            samplingrate = self.samplingrate
        )

    def __repr__(self):
        return '<Hwchassismap %r>' % (self.id)
