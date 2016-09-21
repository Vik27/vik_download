from app import db

class Rawdata(db.Model):

    tablename = "rawdata"

    id = db.Column(db.Integer, primary_key = True)

    livecomponentId = db.Column(db.Integer, db.ForeignKey('livecomponent.id'))

    rawdatasettingId = db.Column(db.Integer, db.ForeignKey('rawdatasetting.id'))

    sliceNo = db.Column(db.Integer)

    data = db.Column(db.BLOB)

    def to_dict(self):
        return dict(
            livecomponentId = self.livecomponentId,
            rawdatasettingId = self.rawdatasettingId,
            sliceNo = self.sliceNo,
            data = self.data,
            id = self.id
        )

    def repr(self):
        return '<Rawdata %r>' % (self.id)