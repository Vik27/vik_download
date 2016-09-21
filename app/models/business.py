from app import db

class Business(db.Model):

    __tablename__ = "business"

    id = db.Column(db.Integer, primary_key = True)
    
    name = db.Column(db.String(20))

    allowedRunProjects = db.Column(db.Integer)

    allowedUsers = db.Column(db.Integer)

    users = db.relationship('User', backref='business', lazy='dynamic')

    devices = db.relationship('Devicetable', backref='business', lazy='dynamic')

    projects = db.relationship('Project', backref='business', lazy='dynamic')

    channeltemplates = db.relationship('Channelsetup', backref='business', lazy='dynamic')

    queues = db.relationship('Queue', backref='business', lazy='dynamic')

    components = db.relationship('Component', backref='business', lazy='dynamic')
    
    def to_dict(self):
        return dict(
            name = self.name,
            allowedRunProjects = self.allowedRunProjects,
            allowedUsers = self.allowedUsers,
            id = self.id
        )

    def __repr__(self):
        return '<Business %r>' % (self.id)
