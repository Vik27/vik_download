from app import db

class Project(db.Model):

    _tablename_ = "project"

    id = db.Column(db.Integer, primary_key = True)
    
    name = db.Column(db.String(20))
    
    timestamp = db.Column(db.DateTime)
    
    description = db.Column(db.String(1000))

    businessId = db.Column(db.Integer,db.ForeignKey('business.id'))

    hwsetupId = db.Column(db.Integer,db.ForeignKey('hardwaresetup.id'))

    componentId = db.Column(db.Integer,db.ForeignKey('component.id'))

    created_byId = db.Column(db.Integer,db.ForeignKey('user.id'))

    # project status
    status = db.Column(db.Enum('incomplete','complete','running'))

    statusChangeDate = db.Column(db.DateTime)

    livecomponentsproject = db.relationship('Livecomponent', backref='project', lazy='dynamic', foreign_keys='Livecomponent.projectId')

    # livecomponentscomponent = db.relationship('Livecomponent', backref='project', lazy='dynamic', foreign_keys='Livecomponent.componentId')

    
    def to_dict(self):
        return dict(
            name = self.name,
            created_on = self.timestamp,
            description = self.description,
            businessId = self.businessId,
            hwsetupId = self.hwsetupId,
            created_byId = self.created_byId,
            status = self.status,
            statusChangeDate = self.statusChangeDate,
            id = self.id
        )

    def _repr_(self):
        return '<Project %r>' % (self.id)