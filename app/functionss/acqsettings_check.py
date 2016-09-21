from app import app, db
from app.models import acquisition, hwchaschanmap, hwchassismap, quantity, unit, Module, channelsetup
import json

def mod_settings_refresh(hwsetupId):
	acqstart = acquisition.Acquisition.query.filter((acquisition.Acquisition.hwsetupId == hwsetupId) & (acquisition.Acquisition.name == 'Start')).first()
	acqstop = acquisition.Acquisition.query.filter((acquisition.Acquisition.hwsetupId == hwsetupId) & (acquisition.Acquisition.name == 'Stop')).first()
	startevent = acqstart.event
	stopevent = acqstop.event
	
	if startevent == 'Digital':
		settngs = json.loads(acqstart.eventValue)
		chanmaprow = hwchaschanmap.Hwchaschanmap.query.get(settngs['digchanmaprowId'])
		if not chanmaprow:
			acqstart.event = 'Free'
			acqstart.eventValue = None
			db.session.commit()

	if startevent == 'Level-based':
		settngs = json.loads(acqstart.eventValue)
		chanmaprow = hwchaschanmap.Hwchaschanmap.query.get(settngs['levchanmaprowId'])
		if not chanmaprow:
			acqstart.event = 'Free'
			acqstart.eventValue = None
			db.session.commit()

	if stopevent == 'Digital':
		settngs = json.loads(acqstop.eventValue)
		chanmaprow = hwchaschanmap.Hwchaschanmap.query.get(settngs['digchanmaprowId'])
		if not chanmaprow:
			acqstop.event = 'Free'
			acqstop.eventValue = None
			db.session.commit()

	if stopevent == 'Level-based':
		settngs = json.loads(acqstop.eventValue)
		chanmaprow = hwchaschanmap.Hwchaschanmap.query.get(settngs['levchanmaprowId'])
		if not chanmaprow:
			acqstop.event = 'Free'
			acqstop.eventValue = None
			db.session.commit()

	acqsettings = {'acqstart': acqstart.to_dict(), 'acqstop': acqstop.to_dict()}
	if acqstart.eventValue:
		acqsettings['acqstart']['eventValue'] = json.loads(acqstart.eventValue)
	if acqstop.eventValue:
		acqsettings['acqstop']['eventValue'] = json.loads(acqstop.eventValue)
	return acqsettings


def chan_settings_refresh(hwsetupId,chanId):
	acqstart = acquisition.Acquisition.query.filter((acquisition.Acquisition.hwsetupId == hwsetupId) & (acquisition.Acquisition.name == 'Start')).first()
	acqstop = acquisition.Acquisition.query.filter((acquisition.Acquisition.hwsetupId == hwsetupId) & (acquisition.Acquisition.name == 'Stop')).first()
	startevent = acqstart.event
	stopevent = acqstop.event
	
	if startevent == 'Digital':
		settngs = json.loads(acqstart.eventValue)
		if (chanId == settngs['digchanmaprowId']):
			chantemp = hwchaschanmap.Hwchaschanmap.query.get(chanId).channelTemplateId
			if not chantemp:
				acqstart.event = 'Free'
				acqstart.eventValue = None
				db.session.commit()

	if startevent == 'Level-based':
		settngs = json.loads(acqstart.eventValue)
		if (chanId == settngs['levchanmaprowId']):
			channel = hwchaschanmap.Hwchaschanmap.query.get(chanId)
			if not channel.channelTemplateId:
				acqstart.event = 'Free'
				acqstart.eventValue = None
				db.session.commit()
			else:
				chanquant = unit.Unit.query.get(channelsetup.Channelsetup.query.get(channel.channelTemplateId).unitId).quantityID
				quantname = quantity.Quantity.query.get(chanquant).name
				if not (quantname == 'Acceleration' or quantname == 'Sound'):
					acqstart.event = 'Free'
					acqstart.eventValue = None
					db.session.commit()
				else:
					if not (settngs['threshold'] <= channel.peakvalue):
						acqstart.event = 'Free'
						acqstart.eventValue = None
						db.session.commit()

	if stopevent == 'Digital':
		settngs = json.loads(acqstop.eventValue)
		if (chanId == settngs['digchanmaprowId']):
			chantemp = hwchaschanmap.Hwchaschanmap.query.get(chanId).channelTemplateId
			if not chantemp:
				acqstop.event = 'Free'
				acqstop.eventValue = None
				db.session.commit()

	if stopevent == 'Level-based':
		settngs = json.loads(acqstop.eventValue)
		if (chanId == settngs['levchanmaprowId']):
			channel = hwchaschanmap.Hwchaschanmap.query.get(chanId)
			if not channel.channelTemplateId:
				acqstop.event = 'Free'
				acqstop.eventValue = None
				db.session.commit()
			else:
				chanquant = unit.Unit.query.get(channelsetup.Channelsetup.query.get(channel.channelTemplateId).unitId).quantityID
				quantname = quantity.Quantity.query.get(chanquant).name
				if not (quantname == 'Acceleration' or quantname == 'Sound'):
					acqstop.event = 'Free'
					acqstop.eventValue = None
					db.session.commit()
				else:
					if not (settngs['threshold'] <= channel.peakvalue):
						acqstop.event = 'Free'
						acqstop.eventValue = None
						db.session.commit()

	acqsettings = {'acqstart': acqstart.to_dict(), 'acqstop': acqstop.to_dict()}
	if acqstart.eventValue:
		acqsettings['acqstart']['eventValue'] = json.loads(acqstart.eventValue)
	if acqstop.eventValue:
		acqsettings['acqstop']['eventValue'] = json.loads(acqstop.eventValue)
	return acqsettings


def acq_editoptions(hwsetupId):

	# acqstart = acquisition.Acquisition.query.filter((acquisition.Acquisition.hwsetupId == hwsetupId) & (acquisition.Acquisition.name == 'Start')).first()
	# acqstop = acquisition.Acquisition.query.filter((acquisition.Acquisition.hwsetupId == hwsetupId) & (acquisition.Acquisition.name == 'Stop')).first()
	# startevent = acqstart.eventValue
	# stopevent = acqstop.eventValue

	free_opts = None
	time_opts = {'time': 5}

	digital_modules = [module.id for module in (Module.Module.query.filter(Module.Module.type == 'Digital_Input').all())]
	level_modules = [module.id for module in (Module.Module.query.filter(Module.Module.type == 'Analog_Input').all())]

	dig_chasmaprows = hwchassismap.Hwchassismap.query.filter\
	((hwchassismap.Hwchassismap.hwSetupID == hwsetupId) & (hwchassismap.Hwchassismap.moduleID.in_(digital_modules))).all()
	lev_chasmaprows = hwchassismap.Hwchassismap.query.filter\
	((hwchassismap.Hwchassismap.hwSetupID == hwsetupId) & (hwchassismap.Hwchassismap.moduleID.in_(level_modules))).all()

	digital_opts = len(dig_chasmaprows)*[None]
	for i in range(len(dig_chasmaprows)):
		dig_chanmaprows = hwchaschanmap.Hwchaschanmap.query.filter\
		(hwchaschanmap.Hwchaschanmap.hwchassId == dig_chasmaprows[len(dig_chasmaprows)-i-1].id).all()
		dig_validchans = len(dig_chanmaprows)*[None]
		for ii in range(len(dig_chanmaprows)):
			if (dig_chanmaprows[len(dig_chanmaprows)-ii-1].channelTemplateId):
				dig_validchans[len(dig_chanmaprows)-ii-1] = dig_chanmaprows[len(dig_chanmaprows)-ii-1].id
			else:
				dig_validchans.pop(len(dig_chanmaprows)-ii-1)
		if (len(dig_validchans) > 0):
			digital_opts[len(dig_chasmaprows)-i-1] = {'slotId': dig_chasmaprows[i].id, 'corres_chanIds': dig_validchans}
		else:
			digital_opts.pop(len(dig_chasmaprows)-i-1)

	level_opts = len(lev_chasmaprows)*[None]
	for i in range(len(lev_chasmaprows)):
		lev_chanmaprows = hwchaschanmap.Hwchaschanmap.query.filter\
		(hwchaschanmap.Hwchaschanmap.hwchassId == lev_chasmaprows[len(lev_chasmaprows)-i-1].id).all()
		lev_validchans = len(lev_chanmaprows)*[None]
		for ii in range(len(lev_chanmaprows)):
			if (lev_chanmaprows[len(lev_chanmaprows)-ii-1].channelTemplateId):
				chanquant = unit.Unit.query.get\
				(channelsetup.Channelsetup.query.get(lev_chanmaprows[len(lev_chanmaprows)-ii-1].channelTemplateId).unitId).quantityID
				quantname = quantity.Quantity.query.get(chanquant).name
				if (quantname == 'Acceleration' or quantname == 'Sound'):
					lev_validchans[len(lev_chanmaprows)-ii-1] = lev_chanmaprows[len(lev_chanmaprows)-ii-1].id
				else:
					lev_validchans.pop(len(lev_chanmaprows)-ii-1)
			else:
				lev_validchans.pop(len(lev_chanmaprows)-ii-1)
		if (len(lev_validchans) > 0):
			level_opts[len(lev_chasmaprows)-i-1] = {'slotId': lev_chasmaprows[i].id, 'corres_chanIds': lev_validchans}
		else:
			level_opts.pop(len(lev_chasmaprows)-i-1)

	acqsettings = [{'name': 'Free', 'description': 'Free or no trigger', 'options': free_opts},
		{'name': 'Time-based', 'description': 'Time-based trigger', 'options': time_opts},
		{'name': 'Digital', 'description': 'Digital input as trigger', 'options': digital_opts},
		{'name': 'Level-based', 'description': 'Threshold level as trigger', 'options': level_opts}]
	if len(level_opts) == 0:
		acqsettings.pop(3)
	if len(digital_opts) == 0:
		acqsettings.pop(2)
	return acqsettings

	# chasmodules = [chasmaprow.moduleID for chasmaprow in chasmaprows]
	# if (len(chasmodules) >= 1):
	# 	modules = Module.Module.query.filter(Module.Module.id.in_(chasmodules)).all()
	# 	modtypes = list(set([module.type for module in modules]))
	# 	len(modtypes)