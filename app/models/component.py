from app import db

class Component(db.Model):

    _tablename_ = "component"

    id = db.Column(db.Integer, primary_key = True)

    productName = db.Column(db.String(128))

    partNo = db.Column(db.String(128))

    productCustomer = db.Column(db.String(128))

    productRemarks = db.Column(db.String(128))

    businessId = db.Column(db.Integer, db.ForeignKey('business.id'))

    projects = db.relationship('Project', backref='component', lazy='dynamic')

    livecomponents = db.relationship('Livecomponent', backref='component', lazy='dynamic')

    def to_dict(self):
        return dict(
            productName = self.productName,
            partNo = self.partNo,
            productCustomer = self.productCustomer,
            productRemarks = self.productRemarks,
            businessId = self.businessId,
            id = self.id
        )

    def _repr_(self):
        return '<Component %r>' % (self.id)