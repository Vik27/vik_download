from app import db

class HardwareSetup(db.Model):

	__tablename__ = "hardwaresetup"
	
	id = db.Column(db.Integer, primary_key = True)
	
	name = db.Column(db.String(20))

	deviceId = db.Column(db.Integer, db.ForeignKey('devicetable.id'))
	
	hwchassmap = db.relationship('Hwchassismap', backref='hwsetup', lazy='dynamic')

	projects = db.relationship('Project', backref='hwsetup', lazy='dynamic')

	status = db.Column(db.Enum('error', 'warning', 'success'))
	# add status of hardwaresetup

	acqId = db.relationship('Acquisition', backref='hwsetup', lazy='dynamic')

	# autorange_time = db.Column(db.Integer)
	# ADD AUTORANGE TIME FOR ANALOG CHANNELS.. ONE VALUE ONLY FOR ALL THE ANALOG CHANNELS

	# trigger = db.Column(db.Integer, db.ForeignKey('hwchaschanmap.id'))
	# ACQUISITON SETTINGS - TRIGGER FOR START, STOP/TIME TO STOP (SAMPLES TO ACQUIRE BEFORE STOP)


	def to_dict(self):
		return dict(
            name = self.name,
            deviceId = self.deviceId,
            # autorange_time = self.autorange_time,
            status = self.status,
            # trigger = self.trigger,
            id = self.id
        )

	def __repr__(self):
                return '<HardwareSetup %r>' % (self.id)
