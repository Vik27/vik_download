from app import db

class Acquisition(db.Model):

	__tablename__ = "acquisition"
	
	id = db.Column(db.Integer, primary_key = True)
	
	name = db.Column(db.Enum('Start', 'Stop'))

	event = db.Column(db.Enum('Free', 'Time-based', 'Digital', 'Level-based'))

	eventValue = db.Column(db.String(256))

	hwsetupId = db.Column(db.Integer, db.ForeignKey('hardwaresetup.id'), nullable=False)

	__table_args__ = (db.UniqueConstraint('hwsetupId','name', name='unique_start_stop'), 
		db.UniqueConstraint('hwsetupId','eventValue', name='unique_startstop_event'),
		)


	def to_dict(self):
		return dict(
			name = self.name,
			event = self.event,
			eventValue = self.eventValue,
			hwsetupId = self.hwsetupId,
			id = self.id
		)

	def __repr__(self):
                return '<Acquisition %r>' % (self.id)
