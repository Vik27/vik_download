from app import db, bcrypt

class User(db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key = True)
    
    username = db.Column(db.String(30))
    
    password = db.Column(db.String(256))
    
    contact_email = db.Column(db.String(50))

    role = db.Column(db.Enum('Admin', 'User', 'Manager'))

    businessId = db.Column(db.Integer,db.ForeignKey('business.id'))

    projects = db.relationship('Project', backref='user', lazy='dynamic')
    

    def __init__(self, username, password, contact_email, role):
        self.username = username
        self.password = bcrypt.generate_password_hash(password)
        self.contact_email = contact_email
        self.role = role


    def to_dict(self):
        return dict(
            username = self.username,
            password = self.password,
            contact_email = self.contact_email,
            role = self.role,
            id = self.id,
            businessId = self.businessId
        )

    def __repr__(self):
        return '<User %r>' % (self.username)


    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)