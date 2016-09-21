from app import db

class Dusratable(db.Model):

    __tablename__ = "dusratable"

    synclogId = db.Column(db.Integer, db.ForeignKey('serversynclog.id'), primary_key = True)

    rowValue = db.Column(db.String(512))

    def to_dict(self):
        return dict(
            synclogId = self.synclogId,
            rowValue = self.rowValue
        )

    def __repr__(self):
        return '<Dusratable %r>' % (self.synclogId)

