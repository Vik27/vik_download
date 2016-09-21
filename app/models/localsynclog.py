from app import db

class Localsynclog(db.Model):

    __tablename__ = "localsynclog"

    id = db.Column(db.Integer, primary_key = True)

    bid = db.Column(db.Integer)

    tablename = db.Column(db.String(20))

    rowid = db.Column(db.Integer)

    type = db.Column(db.Enum('create', 'update', 'delete'))

    
    def to_dict(self):
        return dict(
            tablename = self.tablename,
            rowid = self.rowid,
            type = self.type,
            bid= self.bid,
            id = self.id
        )

    def __repr__(self):
        return '<Serversynlog %r>' % (self.id)
