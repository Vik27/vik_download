from app import app, db
from app.models import acquisition, business, hardwareSetup, devicetable, hwchaschanmap, hwchassismap, Module, unit, channelsetup, quantity
from flask import abort, jsonify, request
import json
from app.functionss import access, hardware_status_check

@app.route('/noviga/businesses/<int:businessId>/hardwareSetups/<int:hwsetupId>/acqsettings', methods = ['PUT'])
def update_biness_acqsettings(businessId,hwsetupId):
	biness = business.Business.query.get(businessId)
	entity = hardwareSetup.HardwareSetup.query.get(hwsetupId)
	if not entity:
		abort(404)
	if not (devicetable.Devicetable.query.get(entity.deviceId).businessId == biness.id):
		abort(404)
	acqstart = acquisition.Acquisition.query.filter\
	((acquisition.Acquisition.hwsetupId == hwsetupId) & (acquisition.Acquisition.name == 'Start')).first()
	if not acqstart:
		abort(404)
	acqstop = acquisition.Acquisition.query.filter\
	((acquisition.Acquisition.hwsetupId == hwsetupId) & (acquisition.Acquisition.name == 'Stop')).first()
	if not acqstop:
		abort(404)
	acqsettings = request.json
	if not (acqsettings['acqstart']):
		abort(404)
	if not (acqsettings['acqstop']):
		abort(404)

	print acqsettings['acqstart']['eventValue']
	acqstart.event = acqsettings['acqstart']['event']
	
	if (acqsettings['acqstart']['event'] == 'Level-based'):
		trigchanId = acqsettings['acqstart']['eventValue']['levchanmaprowId']
		if not trigchanId:
			abort(404)
		trigchan = hwchaschanmap.Hwchaschanmap.query.get(trigchanId)
		if not trigchan:
			abort(404)
		chantempId = trigchan.channelTemplateId
		chanquant = unit.Unit.query.get(channelsetup.Channelsetup.query.get(chantempId).unitId).quantityID
		quantname = quantity.Quantity.query.get(chanquant).name
		if not (quantname == 'Acceleration' or quantname == 'Sound'):
			abort(404)
		chasslotId = trigchan.hwchassId
		chasslot = hwchassismap.Hwchassismap.query.get(chasslotId)
		if not chasslot:
			abort(404)
		if not (chasslot.hwSetupID == hwsetupId):
			abort(404)
		if not acqsettings['acqstart']['eventValue']['threshold']:
			abort(404)
		if not (acqsettings['acqstart']['eventValue']['threshold'] <= trigchan.peakvalue):
			abort(404)
		if not acqsettings['acqstart']['eventValue']['levslope']:
			abort(404)
		acqstart.eventValue = json.dumps(acqsettings['acqstart']['eventValue'])

	elif (acqsettings['acqstart']['event'] == 'Digital'):
		trigchanId = acqsettings['acqstart']['eventValue']['digchanmaprowId']
		if not trigchanId:
			abort(404)
		trigchan = hwchaschanmap.Hwchaschanmap.query.get(trigchanId)
		if not trigchan:
			abort(404)
		chasslotId = trigchan.hwchassId
		chasslot = hwchassismap.Hwchassismap.query.get(chasslotId)
		if not chasslot:
			abort(404)
		if not (chasslot.hwSetupID == hwsetupId):
			abort(404)
		if not (Module.Module.query.get(chasslot.moduleID).type == 'Digital_Input'):
			abort(404)
		if not acqsettings['acqstart']['eventValue']['digslope']:
			abort(404)
		acqstart.eventValue = json.dumps(acqsettings['acqstart']['eventValue'])

	elif (acqsettings['acqstart']['event'] == 'Time-based'):
		if not acqsettings['acqstart']['eventValue']['time']:
			abort(404)
		acqstart.eventValue = json.dumps(acqsettings['acqstart']['eventValue'])

	else:
		acqstart.eventValue = None
	
	# acqstart.eventValue = 'Hello'
	print acqsettings['acqstop']['eventValue']
	acqstop.event = acqsettings['acqstop']['event']
	
	if (acqsettings['acqstop']['event'] == 'Level-based'):
		trigchanId = acqsettings['acqstop']['eventValue']['levchanmaprowId']
		if not trigchanId:
			abort(404)
		trigchan = hwchaschanmap.Hwchaschanmap.query.get(trigchanId)
		if not trigchan:
			abort(404)
		chantempId = trigchan.channelTemplateId
		chanquant = unit.Unit.query.get(channelsetup.Channelsetup.query.get(chantempId).unitId).quantityID
		quantname = quantity.Quantity.query.get(chanquant).name
		if not (quantname == 'Acceleration' or quantname == 'Sound'):
			abort(404)
		chasslotId = trigchan.hwchassId
		chasslot = hwchassismap.Hwchassismap.query.get(chasslotId)
		if not chasslot:
			abort(404)
		if not (chasslot.hwSetupID == hwsetupId):
			abort(404)
		if not acqsettings['acqstop']['eventValue']['threshold']:
			abort(404)
		if not (acqsettings['acqstop']['eventValue']['threshold'] <= trigchan.peakvalue):
			abort(404)
		if not acqsettings['acqstop']['eventValue']['levslope']:
			abort(404)
		acqstop.eventValue = json.dumps(acqsettings['acqstop']['eventValue'])

	elif (acqsettings['acqstop']['event'] == 'Digital'):
		trigchanId = acqsettings['acqstop']['eventValue']['digchanmaprowId']
		if not trigchanId:
			abort(404)
		trigchan = hwchaschanmap.Hwchaschanmap.query.get(trigchanId)
		if not trigchan:
			abort(404)
		chasslotId = trigchan.hwchassId
		chasslot = hwchassismap.Hwchassismap.query.get(chasslotId)
		if not chasslot:
			abort(404)
		if not (chasslot.hwSetupID == hwsetupId):
			abort(404)
		if not (Module.Module.query.get(chasslot.moduleID).type == 'Digital_Input'):
			abort(404)
		if not acqsettings['acqstop']['eventValue']['digslope']:
			abort(404)
		acqstop.eventValue = json.dumps(acqsettings['acqstop']['eventValue'])

	elif (acqsettings['acqstop']['event'] == 'Time-based'):
		if not acqsettings['acqstop']['eventValue']['time']:
			abort(404)
		acqstop.eventValue = json.dumps(acqsettings['acqstop']['eventValue'])
		
	else:
		acqstop.eventValue = None

	# acqstop.eventValue = 'Hell'
	# acqstop.name = 'Start'
	db.session.commit()
	hardware_status_check.hwsetup_check(hwsetupId)
	hwstatus = entity.status
	datatoreturn = {'acqstart': acqstart.to_dict(), 'acqstop': acqstop.to_dict(), 'hwstatus': hwstatus}
	if not (acqstart.event == 'Free'):
		datatoreturn['acqstart']['eventValue'] = json.loads(acqstart.eventValue)
	if not (acqstop.event == 'Free'):
		datatoreturn['acqstop']['eventValue'] = json.loads(acqstop.eventValue)
	return jsonify(datatoreturn)

@app.route('/noviga/hardwareSetups/<int:hwsetupId>/acqsettings', methods = ['PUT'])
def update_acqsettings(hwsetupId):
	acqstart = acquisition.Acquisition.query.filter\
	((acquisition.Acquisition.hwsetupId == hwsetupId) & (acquisition.Acquisition.name == 'Start')).first()
	if not acqstart:
		abort(404)
	acqstop = acquisition.Acquisition.query.filter\
	((acquisition.Acquisition.hwsetupId == hwsetupId) & (acquisition.Acquisition.name == 'Stop')).first()
	if not acqstop:
		abort(404)
	acqsettings = request.json
	if not (acqsettings['acqstart']):
		abort(404)
	if not (acqsettings['acqstop']):
		abort(404)

	print acqsettings['acqstart']['eventValue']
	acqstart.event = acqsettings['acqstart']['event']
	
	if (acqsettings['acqstart']['event'] == 'Level-based'):
		trigchanId = acqsettings['acqstart']['eventValue']['levchanmaprowId']
		if not trigchanId:
			abort(404)
		trigchan = hwchaschanmap.Hwchaschanmap.query.get(trigchanId)
		if not trigchan:
			abort(404)
		chantempId = trigchan.channelTemplateId
		chanquant = unit.Unit.query.get(channelsetup.Channelsetup.query.get(chantempId).unitId).quantityID
		quantname = quantity.Quantity.query.get(chanquant).name
		if not (quantname == 'Acceleration' or quantname == 'Sound'):
			abort(404)
		chasslotId = trigchan.hwchassId
		chasslot = hwchassismap.Hwchassismap.query.get(chasslotId)
		if not chasslot:
			abort(404)
		if not (chasslot.hwSetupID == hwsetupId):
			abort(404)
		if not acqsettings['acqstart']['eventValue']['threshold']:
			abort(404)
		if not (acqsettings['acqstart']['eventValue']['threshold'] <= trigchan.peakvalue):
			abort(404)
		if not acqsettings['acqstart']['eventValue']['levslope']:
			abort(404)
		acqstart.eventValue = json.dumps(acqsettings['acqstart']['eventValue'])

	elif (acqsettings['acqstart']['event'] == 'Digital'):
		trigchanId = acqsettings['acqstart']['eventValue']['digchanmaprowId']
		if not trigchanId:
			abort(404)
		trigchan = hwchaschanmap.Hwchaschanmap.query.get(trigchanId)
		if not trigchan:
			abort(404)
		chasslotId = trigchan.hwchassId
		chasslot = hwchassismap.Hwchassismap.query.get(chasslotId)
		if not chasslot:
			abort(404)
		if not (chasslot.hwSetupID == hwsetupId):
			abort(404)
		if not (Module.Module.query.get(chasslot.moduleID).type == 'Digital_Input'):
			abort(404)
		if not acqsettings['acqstart']['eventValue']['digslope']:
			abort(404)
		acqstart.eventValue = json.dumps(acqsettings['acqstart']['eventValue'])

	elif (acqsettings['acqstart']['event'] == 'Time-based'):
		if not acqsettings['acqstart']['eventValue']['time']:
			abort(404)
		acqstart.eventValue = json.dumps(acqsettings['acqstart']['eventValue'])

	else:
		acqstart.eventValue = None
	
	# acqstart.eventValue = 'Hello'
	print acqsettings['acqstop']['eventValue']
	acqstop.event = acqsettings['acqstop']['event']
	
	if (acqsettings['acqstop']['event'] == 'Level-based'):
		trigchanId = acqsettings['acqstop']['eventValue']['levchanmaprowId']
		if not trigchanId:
			abort(404)
		trigchan = hwchaschanmap.Hwchaschanmap.query.get(trigchanId)
		if not trigchan:
			abort(404)
		chantempId = trigchan.channelTemplateId
		chanquant = unit.Unit.query.get(channelsetup.Channelsetup.query.get(chantempId).unitId).quantityID
		quantname = quantity.Quantity.query.get(chanquant).name
		if not (quantname == 'Acceleration' or quantname == 'Sound'):
			abort(404)
		chasslotId = trigchan.hwchassId
		chasslot = hwchassismap.Hwchassismap.query.get(chasslotId)
		if not chasslot:
			abort(404)
		if not (chasslot.hwSetupID == hwsetupId):
			abort(404)
		if not acqsettings['acqstop']['eventValue']['threshold']:
			abort(404)
		if not (acqsettings['acqstop']['eventValue']['threshold'] <= trigchan.peakvalue):
			abort(404)
		if not acqsettings['acqstop']['eventValue']['levslope']:
			abort(404)
		acqstop.eventValue = json.dumps(acqsettings['acqstop']['eventValue'])

	elif (acqsettings['acqstop']['event'] == 'Digital'):
		trigchanId = acqsettings['acqstop']['eventValue']['digchanmaprowId']
		if not trigchanId:
			abort(404)
		trigchan = hwchaschanmap.Hwchaschanmap.query.get(trigchanId)
		if not trigchan:
			abort(404)
		chasslotId = trigchan.hwchassId
		chasslot = hwchassismap.Hwchassismap.query.get(chasslotId)
		if not chasslot:
			abort(404)
		if not (chasslot.hwSetupID == hwsetupId):
			abort(404)
		if not (Module.Module.query.get(chasslot.moduleID).type == 'Digital_Input'):
			abort(404)
		if not acqsettings['acqstop']['eventValue']['digslope']:
			abort(404)
		acqstop.eventValue = json.dumps(acqsettings['acqstop']['eventValue'])

	elif (acqsettings['acqstop']['event'] == 'Time-based'):
		if not acqsettings['acqstop']['eventValue']['time']:
			abort(404)
		acqstop.eventValue = json.dumps(acqsettings['acqstop']['eventValue'])

	else:
		acqstop.eventValue = None

	# acqstop.eventValue = 'Hell'
	# acqstop.name = 'Start'
	db.session.commit()
	hardware_status_check.hwsetup_check(hwsetupId)
	hwstatus = hardwareSetup.HardwareSetup.query.get(hwsetupId).status
	datatoreturn = {'acqstart': acqstart.to_dict(), 'acqstop': acqstop.to_dict(), 'hwstatus': hwstatus}
	if not (acqstart.event == 'Free'):
		datatoreturn['acqstart']['eventValue'] = json.loads(acqstart.eventValue)
	if not (acqstop.event == 'Free'):
		datatoreturn['acqstop']['eventValue'] = json.loads(acqstop.eventValue)
	return jsonify(datatoreturn)
