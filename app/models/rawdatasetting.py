from app import db

class Rawdatasetting(db.Model):

	_tablename_ = "rawdatasetting"

	id = db.Column(db.Integer, primary_key=True)

	slotId = db.Column(db.Integer)

	samplingrate = db.Column(db.Integer)

	channelNo = db.Column(db.Integer)

	channelName = db.Column(db.Integer)

	peakvalue = db.Column(db.Float)

	chanquantity = db.Column(db.String(128))

	chanunit = db.Column(db.String(128))

	sensitivity = db.Column(db.Float)

	_table_args_ = (db.UniqueConstraint\
		('slotId','samplingrate','channelNo','channelName','peakvalue','chanquantity','chanunit','sensitivity', name='unique_serial_number'), )

	rawdatas = db.relationship('Rawdata', backref='rawdatasetting', lazy='dynamic')

	def to_dict(self):
		return dict(
			id = self.id,
			slotId = self.slotId,
			samplingrate = self.samplingrate,
			channelNo = self.channelNo,
			channelName = self.channelName,
			chanunit = self.chanunit,
			chanquantity = self.chanquantity,
			peakvalue = self.peakvalue,
			sensitivity = self.sensitivity
		)

	def _repr_(self):
		return '<Rawdatasetting %r>' % (self.id)