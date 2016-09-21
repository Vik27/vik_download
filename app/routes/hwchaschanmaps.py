from app import app, db
from app.models import hwchaschanmap, hwchassismap, Module, channelsetup, unit, business, devicetable, hardwareSetup
from flask import abort, jsonify, request
import datetime
import json
from app.functionss import access, acqsettings_check, hardware_status_check


@app.route('/noviga/businesses/<int:businessId>/hwchaschanmaps', methods = ['POST'])
@access.log_required1
@access.business_check
def create_hwchaschanmap(businessId):
    chasmaprowId = request.json['hwchassId']
    if not chasmaprowId:
        abort(404)
    chasmaprow = hwchassismap.Hwchassismap.query.get(chasmaprowId)
    if not chasmaprow:
        abort(404)
    if not (devicetable.Devicetable.query.get(hardwareSetup.HardwareSetup.query.get(chasmaprow.hwSetupID).deviceId).businessId == businessId):
        abort(404)
    module = Module.Module.query.get(hwchassismap.Hwchassismap.query.get(chasmaprowId).moduleID)
    maxchans = module.maxChannels
    quantIds = [x.id for x in module.quants.all()]
    unitIds = [x.id for x in unit.Unit.query.filter(unit.Unit.quantityID.in_(quantIds)).all()]
    chansCreated = hwchaschanmap.Hwchaschanmap.query.filter\
    (hwchaschanmap.Hwchaschanmap.hwchassId == chasmaprowId).all()
    if not chansCreated:
        chanmaprows = request.json['chanmaprows']
        if not (len(chanmaprows) == maxchans):
            abort(404)
        if not (cmp(range(0,maxchans), [x['channelnumber'] for x in chanmaprows]) == 0):
            abort(404)
        datatoreturn = len(chanmaprows)*[None]
        for i in range(len(chanmaprows)):
            entity = hwchaschanmap.Hwchaschanmap(
                channelnumber = chanmaprows[i]['channelnumber']
                , name = chanmaprows[i]['name']
            )

            if not ((chanmaprows[i]['chantempId'] == None) or (chanmaprows[i]['chantempId'] == 'Empty')):
                chantemp = channelsetup.Channelsetup.query.\
                filter((channelsetup.Channelsetup.id == chanmaprows[i]['chantempId']) & (channelsetup.Channelsetup.unitId.in_(unitIds))).first()
                if not chantemp:
                    abort(404)
                xx = chanmaprows[i]['peakvalue']
                if xx:
                    if ((xx <= (module.peakVoltRange*1000.0/chantemp.sensitivity)) and (xx > 0)):
                        entity.peakvalue = xx
                    else:
                        entity.peakvalue = (module.peakVoltRange*1000.0/chantemp.sensitivity)
                else:
                    entity.peakvalue = (module.peakVoltRange*1000.0/chantemp.sensitivity)
                chantemp.hwchaschanmaprows.append(entity)
                db.session.add(chantemp)
            
            chasmaprow.hwchaschanmaps.append(entity)
            db.session.add(chasmaprow)
            db.session.commit()
            datatoreturn[i] = entity.to_dict()
    else:
        abort(404)
    acqoptions = acqsettings_check.acq_editoptions(chasmaprow.hwSetupID)
    hardware_status_check.hwsetup_check(chasmaprow.hwSetupID)
    hwstatus = hardwareSetup.HardwareSetup.query.get(chasmaprow.hwSetupID).status
    objecttoreturn = {'channelsetup': datatoreturn, 'acqoptions': acqoptions, 'hwstatus': hwstatus}
    return jsonify(objecttoreturn), 201


@app.route('/noviga/businesses/<int:businessId>/hwchaschanmaps/<int:id>', methods = ['PUT'])
@access.log_required1
@access.business_check
def update_hwchaschanmap(businessId,id):
    entity = hwchaschanmap.Hwchaschanmap.query.get(id)
    if not entity:
        abort(404)
    chasmaprowId = entity.hwchassId
    chasmaprow = hwchassismap.Hwchassismap.query.get(chasmaprowId)
    if not chasmaprow:
        abort(404)
    if not (devicetable.Devicetable.query.get(hardwareSetup.HardwareSetup.query.get(chasmaprow.hwSetupID).deviceId).businessId == businessId):
        abort(404)
    module = Module.Module.query.get(chasmaprow.moduleID)
    currentchans = hwchaschanmap.Hwchaschanmap.query.filter\
    (hwchaschanmap.Hwchaschanmap.hwchassId == chasmaprowId).all()
    maxchans = module.maxChannels
    if not (len(currentchans) == maxchans):
        abort(404)
    quantIds = [x.id for x in module.quants.all()]
    unitIds = [x.id for x in unit.Unit.query.filter(unit.Unit.quantityID.in_(quantIds)).all()]

    if not ((request.json['chantempId'] == None) or (request.json['chantempId'] == 'Empty')):
        chantemp = channelsetup.Channelsetup.query.\
        filter((channelsetup.Channelsetup.id == request.json['chantempId']) & (channelsetup.Channelsetup.unitId.in_(unitIds))).first()
        if not chantemp:
            abort(404)
        entity.name = request.json['name']
        xx = request.json['peakvalue']
        if xx:
            if ((xx <= (module.peakVoltRange*1000.0/chantemp.sensitivity)) and (xx > 0)):
                entity.peakvalue = xx
            else:
                entity.peakvalue = (module.peakVoltRange*1000.0/chantemp.sensitivity)
        else:
            entity.peakvalue = (module.peakVoltRange*1000.0/chantemp.sensitivity)
        chantemp.hwchaschanmaprows.append(entity)
        db.session.add(chantemp)
    else:
        entity.name = request.json['name']
        if(entity.channelTemplateId):
            entity.peakvalue = None
            currentchantemp = channelsetup.Channelsetup.query.get(entity.channelTemplateId)
            currentchantemp.hwchaschanmaprows.remove(entity)
            db.session.add(currentchantemp)
        db.session.add(entity)
    db.session.commit()
    acqoptions = acqsettings_check.acq_editoptions(chasmaprow.hwSetupID)
    acqsettings = acqsettings_check.chan_settings_refresh(chasmaprow.hwSetupID,id)
    acqstart = acqsettings['acqstart']
    acqstop = acqsettings['acqstop']
    hardware_status_check.hwsetup_check(chasmaprow.hwSetupID)
    hwstatus = hardwareSetup.HardwareSetup.query.get(chasmaprow.hwSetupID).status
    objecttoreturn = {'chansetup': entity.to_dict(), 'acqoptions': acqoptions, 'acqstart': acqstart, 'acqstop': acqstop, 'hwstatus': hwstatus}
    return jsonify(objecttoreturn), 200
