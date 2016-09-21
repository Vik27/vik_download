from app import db

class Livecomponent(db.Model):

    _tablename_ = "livecomponent"

    id = db.Column(db.Integer, primary_key = True)

    projectId = db.Column(db.Integer,db.ForeignKey('project.id'))

    componentId = db.Column(db.Integer,db.ForeignKey('component.id'))

    serialNo = db.Column(db.String(128))

    testedOn = db.Column(db.DateTime)

    result = db.Column(db.Enum('Pass','Fail'))

    rawdatas = db.relationship('Rawdata', backref='livecomponent', lazy='dynamic')

    _table_args_ = (db.UniqueConstraint('projectId','serialNo', name='unique_serial_number'), )

    def to_dict(self):
        return dict(
            projectId = self.projectId,
            componentId = self.componentId,
            serialNo = self.serialNo,
            testedOn = self.testedOn,
            result = self.result,
            id = self.id
        )

    def _repr_(self):
        return '<Livecomponent %r>' % (self.id)