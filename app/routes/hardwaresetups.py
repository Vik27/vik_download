from app import app, db
from app.models import hardwareSetup, hwchassismap, Chassis, Module, devicetable, hwchaschanmap, channelsetup, business, quantity, unit, acquisition
from flask import abort, jsonify, request
import datetime
import json
from app.functionss import access, acqsettings_check, hardware_status_check
from app.routes import rabmsgToClient


@app.route('/noviga/hardwaresetups', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin')
def get_all_hardwaresetups():
    entities = hardwareSetup.HardwareSetup.query.all()
    hwsetups = len(entities)*[None]
    for i in range(len(entities)):
        hwsetups[i] = entities[i].to_dict()
        chassmaprows = hwchassismap.Hwchassismap.query.filter\
        (hwchassismap.Hwchassismap.hwSetupID==entities[i].id).all()
        hwsetups[i]["slotdetails"] = len(chassmaprows)*[None]
        for ii in range(len(chassmaprows)):
            hwsetups[i]["slotdetails"][ii] = chassmaprows[ii].to_dict()
            channels = hwchaschanmap.Hwchaschanmap.query\
            .filter(hwchaschanmap.Hwchaschanmap.hwchassId == chassmaprows[ii].id).all()
            if channels:
                hwsetups[i]["slotdetails"][ii]['chansetupshow'] = True
                hwsetups[i]["slotdetails"][ii]['channelsetup'] = len(channels)*[None]
                for iii in range(len(channels)):
                    hwsetups[i]["slotdetails"][ii]['channelsetup'][iii] = channels[iii].to_dict()
            else:
                hwsetups[i]["slotdetails"][ii]['chansetupshow'] = False
    return json.dumps(hwsetups)


@app.route('/noviga/hardwaresetups/<int:id>', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin')
def get_hardwareSetup(id):
    entity = hardwareSetup.HardwareSetup.query.get(id)
    if not entity:
        abort(404)
    hwsetup=entity.to_dict();
    chassmaprows=hwchassismap.Hwchassismap.query.filter(hwchassismap.Hwchassismap.hwSetupID==id).all()
    hwsetup['slotdetails'] = len(chassmaprows)*[None]
    for i in range(len(chassmaprows)):
        hwsetup['slotdetails'][i] = chassmaprows[i].to_dict()    
    return json.dumps(hwsetup)


@app.route('/noviga/hardwaresetups', methods = ['POST'])
@access.log_required1
@access.requires_roles('Admin')
def create_hardwareSetup():
    if not (request.json['deviceId'] and request.json['name']):
        abort(404)
    device = devicetable.Devicetable.query.get(request.json['deviceId'])
    if not device:
        abort(404)
    if not (request.json['slotdetails']):
        abort(404)
    slots = Chassis.Chassis.query.get(device.niChassisId).maxSlots
    postedslots=request.json['slotdetails']
    if not (len(postedslots) == slots):
        abort(404)
    if not (cmp(range(1,slots+1), [x['slotnumber'] for x in postedslots]) == 0):
        abort(404)
    entity = hardwareSetup.HardwareSetup(name = request.json['name'])
    device.hwsetups.append(entity)
    db.session.add(device)
    acqstart = acquisition.Acquisition(name = 'Start', event = 'Free', eventValue = None)
    acqstop = acquisition.Acquisition(name = 'Stop', event = 'Free', eventValue = None)
    entity.acqId.append(acqstart)
    entity.acqId.append(acqstop)
    entity.status = 'error'
    db.session.add(entity)
    chassmaprows = slots*[None]
    for i in range(slots):
        chassmaprow = hwchassismap.Hwchassismap(slotnumber = postedslots[i]['slotnumber'])
        entity.hwchassmap.append(chassmaprow)
        db.session.add(entity)
        if not ((postedslots[i]['moduleID'] == None) or (postedslots[i]['moduleID'] == 'Empty')):
            module = Module.Module.query.get(postedslots[i]['moduleID'])
            if not module:
                abort(404)
            xx = postedslots[i]['samplingrate']
            if xx:
                if ((not(xx%100)) and (xx <= module.maxSamplingRate) and (xx >= 100)):
                    if (((module.maxSamplingRate/xx) & ((module.maxSamplingRate/xx)-1)) == 0):
                        chassmaprow.samplingrate = xx
                    else:
                        chassmaprow.samplingrate = module.maxSamplingRate
                else:
                    chassmaprow.samplingrate = module.maxSamplingRate
            else:
                chassmaprow.samplingrate = module.maxSamplingRate
            module.hwchassmap.append(chassmaprow)
            db.session.add(module)
        # db.session.commit()
        chassmaprows[i] = chassmaprow.to_dict()
    print [x for x in chassmaprows]
    db.session.commit()
    hwsetup=entity.to_dict();
    hwsetup['slotdetails'] = len(chassmaprows)*[None]
    hwsetup['acqstart'] = acqstart.to_dict()
    hwsetup['acqstop'] = acqstop.to_dict()
    hwsetup['acqoptions'] = acqsettings_check.acq_editoptions(entity.id)
    for i in range(len(chassmaprows)):
        hwsetup['slotdetails'][i] = chassmaprows[i]
        if chassmaprows[i]['moduleID']:
            hwsetup['slotdetails'][i]['samplingchoose'] = False
        else:
            hwsetup['slotdetails'][i]['samplingchoose'] = True
        hwsetup['slotdetails'][i]['chansetupshow'] = False
    return jsonify(hwsetup), 201


@app.route('/noviga/hardwaresetups/<int:id>', methods = ['PUT'])
@access.log_required1
@access.requires_roles('Admin')
def update_hardwareSetup(id):
    entity = hardwareSetup.HardwareSetup.query.get(id)
    if not entity:
        abort(404)
    if not ((request.json['deviceId']) and (request.json['name'])):
        abort(404)
    if not (entity.deviceId == request.json['deviceId']):
        abort(404)
    else:
        device = devicetable.Devicetable.query.get(request.json['deviceId'])
        if not (request.json['slotdetails']):
            abort(404)
        slots = Chassis.Chassis.query.get(device.niChassisId).maxSlots
        postedslots=request.json['slotdetails']
        if not (len(postedslots) == slots):
            abort(404)
        if not (cmp(range(1,slots+1), [x['slotnumber'] for x in postedslots]) == 0):
            abort(404)
        entity.name = request.json['name']
        chassmaprows = slots*[None]
        for i in range(slots):
            chassmaprow = hwchassismap.Hwchassismap.query\
            .filter((hwchassismap.Hwchassismap.hwSetupID==id) & (hwchassismap.Hwchassismap.slotnumber==postedslots[i]['slotnumber'])).first()
            if not ((postedslots[i]['moduleID'] == None) or (postedslots[i]['moduleID'] == 'Empty')):
                if (chassmaprow.moduleID == postedslots[i]['moduleID']):
                    module = Module.Module.query.get(postedslots[i]['moduleID'])
                    xx = postedslots[i]['samplingrate']
                    if xx:
                        if ((not(xx%100)) and (xx <= module.maxSamplingRate) and (xx >= 100)):
                            if (((module.maxSamplingRate/xx) & ((module.maxSamplingRate/xx)-1)) == 0):
                                chassmaprow.samplingrate = xx
                            else:
                                chassmaprow.samplingrate = module.maxSamplingRate
                        else:
                            chassmaprow.samplingrate = module.maxSamplingRate
                    else:
                        chassmaprow.samplingrate = module.maxSamplingRate
                else:
                    module = Module.Module.query.get(postedslots[i]['moduleID'])
                    if not module:
                        abort(404)
                    xx = postedslots[i]['samplingrate']
                    if xx:
                        if ((not(xx%100)) and (xx <= module.maxSamplingRate) and (xx >= 100)):
                            if (((module.maxSamplingRate/xx) & ((module.maxSamplingRate/xx)-1)) == 0):
                                chassmaprow.samplingrate = xx
                            else:
                                chassmaprow.samplingrate = module.maxSamplingRate
                        else:
                            chassmaprow.samplingrate = module.maxSamplingRate
                    else:
                        chassmaprow.samplingrate = module.maxSamplingRate
                    if (chassmaprow.moduleID):
                        channels = hwchaschanmap.Hwchaschanmap.query.filter\
                        (hwchaschanmap.Hwchaschanmap.hwchassId == chassmaprow.id).all()
                        for channel in channels:
                            db.session.delete(channel)
                    module.hwchassmap.append(chassmaprow)
                    db.session.add(module)
            else:
                if (chassmaprow.moduleID):
                    chassmaprow.samplingrate = None
                    channels = hwchaschanmap.Hwchaschanmap.query.filter\
                    (hwchaschanmap.Hwchaschanmap.hwchassId == chassmaprow.id).all()
                    for channel in channels:
                        db.session.delete(channel)
                    module = Module.Module.query.get(chassmaprow.moduleID)
                    module.hwchassmap.remove(chassmaprow)
                    db.session.add(module)
                else:
                    pass
            db.session.commit()
            chassmaprows[i] = chassmaprow.to_dict()
    
    db.session.commit()
    acqsettings = acqsettings_check.mod_settings_refresh(entity.id)
    hardware_status_check.hwsetup_check(id)
    hwsetup=entity.to_dict()
    # acqstart = acquisition.Acquisition.query.filter((acquisition.Acquisition.name == 'Start') & (acquisition.Acquisition.hwsetupId == entity.id)).first()
    # acqstop = acquisition.Acquisition.query.filter((acquisition.Acquisition.name == 'Stop') & (acquisition.Acquisition.hwsetupId == entity.id)).first()
    # hwsetup['acqstart'] = acqstart.to_dict()
    # hwsetup['acqstop'] = acqstop.to_dict()
    hwsetup['acqstart'] = acqsettings['acqstart']
    hwsetup['acqstop'] = acqsettings['acqstop']
    hwsetup['acqoptions'] = acqsettings_check.acq_editoptions(entity.id)
    hwsetup['slotdetails'] = len(chassmaprows)*[None]
    for i in range(len(chassmaprows)):
        hwsetup['slotdetails'][i] = chassmaprows[i]
        if chassmaprows[i]['moduleID']:
            hwsetup['slotdetails'][i]['samplingchoose'] = False
        else:
            hwsetup['slotdetails'][i]['samplingchoose'] = True
        channels = hwchaschanmap.Hwchaschanmap.query\
        .filter(hwchaschanmap.Hwchaschanmap.hwchassId == chassmaprows[i]['id']).all()
        if channels:
            hwsetup["slotdetails"][i]['chansetupshow'] = True
            hwsetup["slotdetails"][i]['channelsetup'] = len(channels)*[None]
            for ii in range(len(channels)):
                hwsetup["slotdetails"][i]['channelsetup'][ii] = channels[ii].to_dict()
        else:
            hwsetup['slotdetails'][i]['chansetupshow'] = False
    return jsonify(hwsetup), 200


@app.route('/noviga/hardwaresetups/<int:id>', methods = ['DELETE'])
@access.log_required1
@access.requires_roles('Admin')
def delete_hardwareSetup(id):
    entity = hardwareSetup.HardwareSetup.query.get(id)
    if not entity:
        abort(404)
    acqstart = acquisition.Acquisition.query.filter((acquisition.Acquisition.name == 'Start') & (acquisition.Acquisition.hwsetupId == entity.id)).first()
    acqstop = acquisition.Acquisition.query.filter((acquisition.Acquisition.name == 'Stop') & (acquisition.Acquisition.hwsetupId == entity.id)).first()
    entities1=hwchassismap.Hwchassismap.query.filter(hwchassismap.Hwchassismap.hwSetupID==id).all()
    if not entities1:
        abort(404)
    for entity1 in entities1:
        channels = hwchaschanmap.Hwchaschanmap.query.filter\
        (hwchaschanmap.Hwchaschanmap.hwchassId == entity1.id).all()
        for channel in channels:
            db.session.delete(channel)
        db.session.delete(entity1)
    db.session.delete(acqstart)
    db.session.delete(acqstop)
    db.session.delete(entity)
    db.session.commit()
    return '', 204


@app.route('/noviga/businesses/<int:businessId>/hardwaresetups', methods = ['GET'])
@access.log_required1
@access.business_check
def get_biness_hardwaresetups(businessId):
    binessdeviceIds = [x.id for x in devicetable.Devicetable.query.filter\
    (devicetable.Devicetable.businessId == businessId).all()]
    if (len(binessdeviceIds) >= 1):
        entities = hardwareSetup.HardwareSetup.query.filter\
        (hardwareSetup.HardwareSetup.deviceId.in_(binessdeviceIds)).all()
    else:
        entities = [];
    hwsetups = len(entities)*[None]
    for i in range(len(entities)):
        hwsetups[i] = entities[i].to_dict()
        chassmaprows = hwchassismap.Hwchassismap.query.filter\
        (hwchassismap.Hwchassismap.hwSetupID==entities[i].id).all()
        hwsetups[i]["slotdetails"] = len(chassmaprows)*[None]
        for ii in range(len(chassmaprows)):
            hwsetups[i]["slotdetails"][ii] = chassmaprows[ii].to_dict()
            channels = hwchaschanmap.Hwchaschanmap.query\
            .filter(hwchaschanmap.Hwchaschanmap.hwchassId == chassmaprows[ii].id).all()
            if channels:
                hwsetups[i]["slotdetails"][ii]['chansetupshow'] = True
                hwsetups[i]["slotdetails"][ii]['channelsetup'] = len(channels)*[None]
                for iii in range(len(channels)):
                    hwsetups[i]["slotdetails"][ii]['channelsetup'][iii] = channels[iii].to_dict()
            else:
                hwsetups[i]["slotdetails"][ii]['chansetupshow'] = False
    return json.dumps(hwsetups)


@app.route('/noviga/businesses/<int:businessId>/hardwaresetups/<int:id>', methods = ['GET'])
@access.log_required1
@access.business_check
def get_biness_hardwaresetup(businessId,id):
    biness = business.Business.query.get(businessId)
    entity = hardwareSetup.HardwareSetup.query.get(id)
    if not entity:
        abort(404)
    if not (devicetable.Devicetable.query.get(entity.deviceId).businessId == biness.id):
        abort(404)
    hwsetup=entity.to_dict();
    chassmaprows=hwchassismap.Hwchassismap.query.filter(hwchassismap.Hwchassismap.hwSetupID==id).all()
    hwsetup['slotdetails'] = len(chassmaprows)*[None]
    for i in range(len(chassmaprows)):
        hwsetup['slotdetails'][i] = chassmaprows[i].to_dict()    
    return json.dumps(hwsetup)


@app.route('/noviga/businesses/<int:businessId>/hardwaresetups', methods = ['POST'])
@access.log_required1
@access.business_check
def create_biness_hardwaresetup(businessId):
    biness = business.Business.query.get(businessId)
    if not (request.json['deviceId'] and request.json['name']):
        abort(404)
    device = devicetable.Devicetable.query.get(request.json['deviceId'])
    if not device:
        abort(404)
    if not (device.businessId == biness.id):
        abort(404)
    if not (request.json['slotdetails']):
        abort(404)
    slots = Chassis.Chassis.query.get(device.niChassisId).maxSlots
    postedslots=request.json['slotdetails']
    if not (len(postedslots) == slots):
        abort(404)
    if not (cmp(range(1,slots+1), [x['slotnumber'] for x in postedslots]) == 0):
        abort(404)
    entity = hardwareSetup.HardwareSetup(name = request.json['name'])
    device.hwsetups.append(entity)
    db.session.add(device)
    acqstart = acquisition.Acquisition(name = 'Start', event = 'Free', eventValue = None)
    acqstop = acquisition.Acquisition(name = 'Stop', event = 'Free', eventValue = None)
    entity.acqId.append(acqstart)
    entity.acqId.append(acqstop)
    entity.status = 'error'
    db.session.add(entity)
    chassmaprows = slots*[None]
    for i in range(slots):
        chassmaprow = hwchassismap.Hwchassismap(slotnumber = postedslots[i]['slotnumber'])
        entity.hwchassmap.append(chassmaprow)
        db.session.add(entity)
        if not ((postedslots[i]['moduleID'] == None) or (postedslots[i]['moduleID'] == 'Empty')):
            module = Module.Module.query.get(postedslots[i]['moduleID'])
            if not module:
                abort(404)
            xx = postedslots[i]['samplingrate']
            if xx:
                if ((not(xx%100)) and (xx <= module.maxSamplingRate) and (xx >= 100)):
                    if (((module.maxSamplingRate/xx) & ((module.maxSamplingRate/xx)-1)) == 0):
                        chassmaprow.samplingrate = xx
                    else:
                        chassmaprow.samplingrate = module.maxSamplingRate
                else:
                    chassmaprow.samplingrate = module.maxSamplingRate
            else:
                chassmaprow.samplingrate = module.maxSamplingRate
            module.hwchassmap.append(chassmaprow)
            db.session.add(module)

        db.session.commit()
        chassmaprows[i] = chassmaprow.to_dict()
    db.session.commit()
    hwsetup=entity.to_dict();
    hwsetup['slotdetails'] = len(chassmaprows)*[None]
    hwsetup['acqstart'] = acqstart.to_dict()
    hwsetup['acqstop'] = acqstop.to_dict()
    hwsetup['acqoptions'] = acqsettings_check.acq_editoptions(entity.id)
    for i in range(len(chassmaprows)):
        hwsetup['slotdetails'][i] = chassmaprows[i]
        if chassmaprows[i]['moduleID']:
            hwsetup['slotdetails'][i]['samplingchoose'] = False
        else:
            hwsetup['slotdetails'][i]['samplingchoose'] = True
        hwsetup['slotdetails'][i]['chansetupshow'] = False
    return jsonify(hwsetup), 201


@app.route('/noviga/businesses/<int:businessId>/hardwaresetups/<int:id>', methods = ['PUT'])
@access.log_required1
@access.business_check
def update_biness_hardwaresetup(businessId,id):
    entity = hardwareSetup.HardwareSetup.query.get(id)
    if not entity:
        abort(404)
    if not ((request.json['deviceId']) and (request.json['name'])):
        abort(404)
    if not (entity.deviceId == request.json['deviceId']):
        abort(404)
    else:
        device = devicetable.Devicetable.query.get(request.json['deviceId'])
        if not (request.json['slotdetails']):
            abort(404)
        slots = Chassis.Chassis.query.get(device.niChassisId).maxSlots
        postedslots=request.json['slotdetails']
        if not (len(postedslots) == slots):
            abort(404)
        if not (cmp(range(1,slots+1), [x['slotnumber'] for x in postedslots]) == 0):
            abort(404)
        entity.name = request.json['name']
        for i in range(slots):
            chassmaprow = hwchassismap.Hwchassismap.query\
            .filter((hwchassismap.Hwchassismap.hwSetupID==id) & (hwchassismap.Hwchassismap.slotnumber==postedslots[i]['slotnumber'])).first()
            if not ((postedslots[i]['moduleID'] == None) or (postedslots[i]['moduleID'] == 'Empty')):
                if (chassmaprow.moduleID == postedslots[i]['moduleID']):
                    module = Module.Module.query.get(postedslots[i]['moduleID'])
                    xx = postedslots[i]['samplingrate']
                    if xx:
                        eprint(xx)
                        if ((not(xx%100)) and (xx <= module.maxSamplingRate) and (xx >= 100)):
                            if (((module.maxSamplingRate/xx) & ((module.maxSamplingRate/xx)-1)) == 0):
                                chassmaprow.samplingrate = xx
                            else:
                                chassmaprow.samplingrate = module.maxSamplingRate
                        else:
                            chassmaprow.samplingrate = module.maxSamplingRate
                    else:
                        chassmaprow.samplingrate = module.maxSamplingRate
                else:
                    module = Module.Module.query.get(postedslots[i]['moduleID'])
                    if not module:
                        abort(404)
                    xx = postedslots[i]['samplingrate']
                    if ((not(xx%100)) and (xx <= module.maxSamplingRate) and (xx >= 100)):
                        if (((module.maxSamplingRate/xx) & ((module.maxSamplingRate/xx)-1)) == 0):
                            chassmaprow.samplingrate = xx
                        else:
                            chassmaprow.samplingrate = module.maxSamplingRate
                    else:
                        chassmaprow.samplingrate = module.maxSamplingRate
                    if (chassmaprow.moduleID):
                        channels = hwchaschanmap.Hwchaschanmap.query.filter\
                        (hwchaschanmap.Hwchaschanmap.hwchassId == chassmaprow.id).all()
                        for channel in channels:
                            db.session.delete(channel)
                    module.hwchassmap.append(chassmaprow)
                    db.session.add(module)
            else:
                if (chassmaprow.moduleID):
                    channels = hwchaschanmap.Hwchaschanmap.query.filter\
                    (hwchaschanmap.Hwchaschanmap.hwchassId == chassmaprow.id).all()
                    for channel in channels:
                        db.session.delete(channel)
                    module = Module.Module.query.get(chassmaprow.moduleID)
                    module.hwchassmap.remove(chassmaprow)
                    chassmaprow.samplingrate = None
                    db.session.add(module)
                else:
                    pass
            db.session.commit()
            chassmaprows[i] = chassmaprow.to_dict()
    
    db.session.commit()
    acqsettings = acqsettings_check.mod_settings_refresh(entity.id)
    hardware_status_check.hwsetup_check(id)
    hwsetup=entity.to_dict()
    hwsetup['acqstart'] = acqsettings['acqstart']
    hwsetup['acqstop'] = acqsettings['acqstop']
    hwsetup['acqoptions'] = acqsettings_check.acq_editoptions(entity.id)
    hwsetup['slotdetails'] = len(chassmaprows)*[None]
    for i in range(len(chassmaprows)):
        hwsetup['slotdetails'][i] = chassmaprows[i]
        if chassmaprows[i]['moduleID']:
            hwsetup['slotdetails'][i]['samplingchoose'] = False
        else:
            hwsetup['slotdetails'][i]['samplingchoose'] = True
        channels = hwchaschanmap.Hwchaschanmap.query\
        .filter(hwchaschanmap.Hwchaschanmap.hwchassId == chassmaprows[i]['id']).all()
        if channels:
            hwsetup["slotdetails"][i]['chansetupshow'] = True
            hwsetup["slotdetails"][i]['channelsetup'] = len(channels)*[None]
            for ii in range(len(channels)):
                hwsetup["slotdetails"][i]['channelsetup'][ii] = channels[ii].to_dict()
        else:
            hwsetup['slotdetails'][i]['chansetupshow'] = False
    db.session.commit()
    return jsonify(entity.to_dict()), 200


@app.route('/noviga/businesses/<int:businessId>/hardwaresetups/<int:id>', methods = ['DELETE'])
@access.log_required1
@access.business_check
def delete_biness_hardwaresetup(businessId,id):
    biness = business.Business.query.get(businessId)
    entity = hardwareSetup.HardwareSetup.query.get(id)
    if not entity:
        abort(404)
    if not (devicetable.Devicetable.query.get(entity.deviceId).businessId == biness.id):
        abort(404)
    acqstart = acquisition.Acquisition.query.filter((acquisition.Acquisition.name == 'Start') & (acquisition.Acquisition.hwsetupId == entity.id)).first()
    acqstop = acquisition.Acquisition.query.filter((acquisition.Acquisition.name == 'Stop') & (acquisition.Acquisition.hwsetupId == entity.id)).first()
    entities1=hwchassismap.Hwchassismap.query.filter(hwchassismap.Hwchassismap.hwSetupID==id).all()
    if not entities1:
        abort(404)
    for entity1 in entities1:
        channels = hwchaschanmap.Hwchaschanmap.query.filter\
        (hwchaschanmap.Hwchaschanmap.hwchassId == entity1.id).all()
        for channel in channels:
            db.session.delete(channel)
        db.session.delete(entity1)
    db.session.delete(acqstart)
    db.session.delete(acqstop)
    db.session.delete(entity)
    db.session.commit()
    return '', 204


@app.route('/noviga/businesses/all/hwsetupsdata', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin')
def get_allbiness_hwsetupsdata():
    hw_entities = hardwareSetup.HardwareSetup.query.all()
    hwsetups = len(hw_entities)*[None]
    for i in range(len(hw_entities)):
        hwsetups[i] = hw_entities[i].to_dict()
        acqstart = acquisition.Acquisition.query.filter((acquisition.Acquisition.name == 'Start') & (acquisition.Acquisition.hwsetupId == hw_entities[i].id)).first()
        acqstop = acquisition.Acquisition.query.filter((acquisition.Acquisition.name == 'Stop') & (acquisition.Acquisition.hwsetupId == hw_entities[i].id)).first()
        hwsetups[i]['acqstart'] = acqstart.to_dict()
        print hwsetups[i]['acqstart']
        if acqstart.eventValue:
            hwsetups[i]['acqstart']['eventValue'] = json.loads(acqstart.eventValue)
        hwsetups[i]['acqstop'] = acqstop.to_dict()
        print hwsetups[i]['acqstop']
        if acqstop.eventValue:
            hwsetups[i]['acqstop']['eventValue'] = json.loads(acqstop.eventValue)
        hwsetups[i]['acqoptions'] = acqsettings_check.acq_editoptions(hw_entities[i].id)
        chassmaprows = hwchassismap.Hwchassismap.query.filter\
        (hwchassismap.Hwchassismap.hwSetupID==hw_entities[i].id).all()
        hwsetups[i]["slotdetails"] = len(chassmaprows)*[None]
        for ii in range(len(chassmaprows)):
            hwsetups[i]["slotdetails"][ii] = chassmaprows[ii].to_dict()
            if chassmaprows[ii].moduleID:
                # samplingchoose if for disabling sampling in front end
                hwsetups[i]["slotdetails"][ii]['samplingchoose'] = False
            else:
                hwsetups[i]["slotdetails"][ii]['samplingchoose'] = True
            channels = hwchaschanmap.Hwchaschanmap.query\
            .filter(hwchaschanmap.Hwchaschanmap.hwchassId == chassmaprows[ii].id).all()
            if channels:
                hwsetups[i]["slotdetails"][ii]['chansetupshow'] = True
                hwsetups[i]["slotdetails"][ii]['channelsetup'] = len(channels)*[None]
                for iii in range(len(channels)):
                    hwsetups[i]["slotdetails"][ii]['channelsetup'][iii] = channels[iii].to_dict()
            else:
                hwsetups[i]["slotdetails"][ii]['chansetupshow'] = False
    
    chas_entities = Chassis.Chassis.query.all()
    chassises = len(chas_entities)*[None]
    for i in range(len(chas_entities)):
        chassises[i] = chas_entities[i].to_dict()
   
    mod_entities = Module.Module.query.all()
    modules = len(mod_entities)*[None]
    for ii in range(len(mod_entities)):
        modules[ii] = mod_entities[ii].to_dict()
        quantis = mod_entities[ii].quants.all()
        modules[ii]["quantities"] = len(quantis)*[None]
        for iii in range(len(quantis)):
            modules[ii]["quantities"][iii] = quantis[iii].to_dict()
   
    quant_entities = quantity.Quantity.query.all()
    quantities = len(quant_entities)*[None]
    for i in range(len(quant_entities)):
        quantities[i] = quant_entities[i].to_dict()
        units = unit.Unit.query.filter(unit.Unit.quantityID == quant_entities[i].id).all()
        quantities[i]["units"] = len(units)*[None]
        for ii in range(len(units)):
            quantities[i]["units"][ii] = units[ii].to_dict()

    unit_entities = unit.Unit.query.all()
    units = len(unit_entities)*[None]
    for i in range(len(unit_entities)):
        units[i] = unit_entities[i].to_dict()
    
    bus_entities = business.Business.query.all()
    businesses = len(bus_entities)*[None]
    for i in range(len(bus_entities)):
        businesses[i] = bus_entities[i].to_dict()
    
    dev_entities = devicetable.Devicetable.query.all()
    devices = len(dev_entities)*[None]
    for i in range(len(dev_entities)):
        devices[i] = dev_entities[i].to_dict()
    
    chan_entities = channelsetup.Channelsetup.query.all()
    chansetups = len(chan_entities)*[None]
    for i in range(len(chan_entities)):
        chansetups[i] = chan_entities[i].to_dict()
        chansetups[i]["quantityId"] = \
        (unit.Unit.query.filter(unit.Unit.id==chansetups[i]["unitId"]).first().to_dict())["quantityID"]

    hwsetupsdata = {'hwsetups': hwsetups, 'chassises': chassises, 'modules': modules, 'devices': devices, 'businesses': businesses, 'chansetups': chansetups, 'quantities': quantities, 'units': units}
    return jsonify(hwsetupsdata)



@app.route('/noviga/businesses/<int:businessId>/hwsetupsdata', methods = ['GET'])
@access.log_required1
@access.business_check
def get_biness_hwsetupsdata(businessId):
    binessdeviceIds = [x.id for x in devicetable.Devicetable.query.filter\
    (devicetable.Devicetable.businessId == businessId).all()]
    if (len(binessdeviceIds) >= 1):
        hw_entities = hardwareSetup.HardwareSetup.query.filter\
        (hardwareSetup.HardwareSetup.deviceId.in_(binessdeviceIds)).all()
    else:
        hw_entities = [];
    hwsetups = len(hw_entities)*[None]
    for i in range(len(hw_entities)):
        hwsetups[i] = hw_entities[i].to_dict()
        acqstart = acquisition.Acquisition.query.filter((acquisition.Acquisition.name == 'Start') & (acquisition.Acquisition.hwsetupId == hw_entities[i].id)).first()
        acqstop = acquisition.Acquisition.query.filter((acquisition.Acquisition.name == 'Stop') & (acquisition.Acquisition.hwsetupId == hw_entities[i].id)).first()
        hwsetups[i]['acqstart'] = acqstart.to_dict()
        print acqstart.eventValue
        if acqstart.eventValue:
            hwsetups[i]['acqstart']['eventValue'] = json.loads(acqstart.eventValue)
        print json.loads(acqstart.eventValue)
        hwsetups[i]['acqstop'] = acqstop.to_dict()
        if acqstop.eventValue:
            hwsetups[i]['acqstop']['eventValue'] = json.loads(acqstop.eventValue)
        hwsetups[i]['acqoptions'] = acqsettings_check.acq_editoptions(hw_entities[i].id)
        chassmaprows = hwchassismap.Hwchassismap.query.filter\
        (hwchassismap.Hwchassismap.hwSetupID==hw_entities[i].id).all()
        hwsetups[i]["slotdetails"] = len(chassmaprows)*[None]
        for ii in range(len(chassmaprows)):
            hwsetups[i]["slotdetails"][ii] = chassmaprows[ii].to_dict()
            if chassmaprows[ii].moduleID:
                # samplingchoose if for disabling sampling in front end
                hwsetups[i]["slotdetails"][ii]['samplingchoose'] = False
            else:
                hwsetups[i]["slotdetails"][ii]['samplingchoose'] = True
            channels = hwchaschanmap.Hwchaschanmap.query\
            .filter(hwchaschanmap.Hwchaschanmap.hwchassId == chassmaprows[ii].id).all()
            if channels:
                hwsetups[i]["slotdetails"][ii]['chansetupshow'] = True
                hwsetups[i]["slotdetails"][ii]['channelsetup'] = len(channels)*[None]
                for iii in range(len(channels)):
                    hwsetups[i]["slotdetails"][ii]['channelsetup'][iii] = channels[iii].to_dict()
            else:
                hwsetups[i]["slotdetails"][ii]['chansetupshow'] = False

    # hw_entities = hardwareSetup.HardwareSetup.query.all()
    # hwsetups = len(hw_entities)*[None]
    # for i in range(len(hw_entities)):
    #     hwsetups[i] = hw_entities[i].to_dict()
    #     chassmaprows = hwchassismap.Hwchassismap.query.filter\
    #     (hwchassismap.Hwchassismap.hwSetupID==hw_entities[i].id).all()
    #     hwsetups[i]["slotdetails"] = len(chassmaprows)*[None]
    #     for ii in range(len(chassmaprows)):
    #         hwsetups[i]["slotdetails"][ii] = chassmaprows[ii].to_dict()
    #         channels = hwchaschanmap.Hwchaschanmap.query\
    #         .filter(hwchaschanmap.Hwchaschanmap.hwchassId == chassmaprows[ii].id).all()
    #         if channels:
    #             hwsetups[i]["slotdetails"][ii]['chansetupshow'] = True
    #             hwsetups[i]["slotdetails"][ii]['channelsetup'] = len(channels)*[None]
    #             for iii in range(len(channels)):
    #                 hwsetups[i]["slotdetails"][ii]['channelsetup'][iii] = channels[iii].to_dict()
    #         else:
    #             hwsetups[i]["slotdetails"][ii]['chansetupshow'] = False
    
    chas_entities = Chassis.Chassis.query.all()
    chassises = len(chas_entities)*[None]
    for i in range(len(chas_entities)):
        chassises[i] = chas_entities[i].to_dict()
   
    mod_entities = Module.Module.query.all()
    modules = len(mod_entities)*[None]
    for ii in range(len(mod_entities)):
        modules[ii] = mod_entities[ii].to_dict()
        quantis = mod_entities[ii].quants.all()
        modules[ii]["quantities"] = len(quantis)*[None]
        for iii in range(len(quantis)):
            modules[ii]["quantities"][iii] = quantis[iii].to_dict()
   
    quant_entities = quantity.Quantity.query.all()
    quantities = len(quant_entities)*[None]
    for i in range(len(quant_entities)):
        quantities[i] = quant_entities[i].to_dict()
        units = unit.Unit.query.filter(unit.Unit.quantityID == quant_entities[i].id).all()
        quantities[i]["units"] = len(units)*[None]
        for ii in range(len(units)):
            quantities[i]["units"][ii] = units[ii].to_dict()
    
    # bus_entities = business.Business.query.all()
    # businesses = len(bus_entities)*[None]
    # for i in range(len(bus_entities)):
    #     businesses[i] = bus_entities[i].to_dict()
    
    dev_entities = devicetable.Devicetable.query.filter(devicetable.Devicetable.businessId == businessId).all()
    devices = len(dev_entities)*[None]
    for i in range(len(dev_entities)):
        devices[i] = dev_entities[i].to_dict()
    
    chan_entities = channelsetup.Channelsetup.query.filter(devicetable.Devicetable.businessId == businessId).all()
    chansetups = len(chan_entities)*[None]
    for i in range(len(chan_entities)):
        chansetups[i] = chan_entities[i].to_dict()
        chansetups[i]["quantityId"] = \
        (unit.Unit.query.filter(unit.Unit.id==chansetups[i]["unitId"]).first().to_dict())["quantityID"]

    hwsetupsdata = {'hwsetups': hwsetups, 'chassises': chassises, 'modules': modules, 'devices': devices, 'chansetups': chansetups, 'quantities': quantities}
    return jsonify(hwsetupsdata)



@app.route('/noviga/businesses/<int:businessId>/verifyhwsetup/<int:id>', methods = ['GET'])
@access.log_required1
@access.business_check
def get_biness_verifyhwsetup(businessId,id):
    [reply, devices, hwsetupID]=rabmsgToClient.verifyhw(id)
    toreturn = {'verification': reply}
    return jsonify(toreturn),200

@app.route('/noviga/verifyhwsetup/<int:id>', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin')
def get_verifyhwsetup(id):
    [reply, devices, hwsetupID, qname]=rabmsgToClient.verifyhw(id)
    #print ('yaya' + reply)
    toreturn = {'verification': reply}
    print reply
    return jsonify(toreturn),200
    #return 'hi'

