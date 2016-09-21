from app import db
# from channelnumbertemplate import channelnumbertemplate
from app.models import serversynclog
class Channelsetup(db.Model,serversynclog._BaseMixin):

    __tablename__ = "channelsetup"

    id = db.Column(db.Integer, primary_key = True)
    
    name = db.Column(db.String(20))
    
    # samplingrate = db.Column(db.Integer) moved to hwchassismap for a given module
    
    sensitivity = db.Column(db.Float)
    
    # autorangetime = db.Column(db.Integer)
    
    # peakvalue = db.Column(db.Float)

    unitId = db.Column(db.Integer,db.ForeignKey('unit.id'))

    businessId = db.Column(db.Integer,db.ForeignKey('business.id'))

    hwchaschanmaprows = db.relationship('Hwchaschanmap', backref='hwchaschan', lazy='dynamic')
    

    def to_dict(self):
        return dict(
            name = self.name,
            # samplingrate = self.samplingrate,
            sensitivity = self.sensitivity,
            # autorangetime = self.autorangetime,
            # peakvalue = self.peakvalue,
            id = self.id,
            unitId = self.unitId,
            businessId = self.businessId
        )

    def __repr__(self):
        return '<Channelsetup %r>' % (self.id)
