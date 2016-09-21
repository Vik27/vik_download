from app import app, db
from app.models import hardwareSetup, hwchaschanmap, hwchassismap, acquisition

def hwsetup_check(hwsetupId):
	hwsetup = hardwareSetup.HardwareSetup.query.get(hwsetupId)
	chasmaprows = hwchassismap.Hwchassismap.query.filter\
	((hwchassismap.Hwchassismap.hwSetupID == hwsetupId) & (hwchassismap.Hwchassismap.moduleID != None)).all()
	if not chasmaprows:
		hwsetup.status = 'error'
	else:
		chanflag = 0
		for i in range(len(chasmaprows)):
			channels = hwchaschanmap.Hwchaschanmap.query.filter\
			((hwchaschanmap.Hwchaschanmap.hwchassId == chasmaprows[i].id) & (hwchaschanmap.Hwchaschanmap.channelTemplateId != None)).all()
			if not channels:
				chanflag = chanflag + 0
			else:
				chanflag = chanflag + 1
		if chanflag == 0:
			hwsetup.status = 'error'
		else:
			hwsetup.status = 'warning'
			acqstart = acquisition.Acquisition.query.filter\
			((acquisition.Acquisition.hwsetupId == hwsetupId) & (acquisition.Acquisition.name == 'Start')).first()
			acqstop = acquisition.Acquisition.query.filter\
			((acquisition.Acquisition.hwsetupId == hwsetupId) & (acquisition.Acquisition.name == 'Stop')).first()
			if not (acqstart.event == 'Free' or acqstop.event == 'Free'):
				hwsetup.status = 'success'

	db.session.commit()


