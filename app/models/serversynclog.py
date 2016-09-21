from app import db


class _BaseMixin(object):
    """ Just a helper mixin class to set properties on object creation.  
    Also provides a convenient default __repr__() function, but be aware that 
    also relationships are printed, which might result in loading relations.
    """
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return "<%s(%s)>" % (self.__class__.__name__, 
            ', '.join('%s=%r' % (k, self.__dict__[k]) 
                for k in sorted(self.__dict__) if '_sa_' != k[:4] and '_backref_' != k[:9])
            )


class Serversynclog(db.Model, _BaseMixin):

    __tablename__ = "serversynclog"

    id = db.Column(db.Integer, primary_key = True)

    bid = db.Column(db.Integer)

    tablename = db.Column(db.String(20))

    rowid = db.Column(db.Integer)

    type = db.Column(db.Enum('create', 'update', 'delete'))

    filename=db.Column(db.String(128))

    idtype=db.Column(db.Enum('local', 'global'))

    dusratablerows = db.relationship('Dusratable', backref='serversynclog', lazy='dynamic')

    
    def to_dict(self):
        return dict(
            tablename = self.tablename,
            rowid = self.rowid,
            type = self.type,
            bid= self.bid,
            id = self.id,
            filename=self.filename,
            idtype=self.idtype

        )

    def __repr__(self):
        return '<Serversynlog %r>' % (self.id)

