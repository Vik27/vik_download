from app import app, db
from app.models import devicetable, business, Chassis, queue
from flask import abort, jsonify, request
import datetime
import json
from app.functionss import access


@app.route('/noviga/devices/all', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin')
def get_devicesdata():
    dev_entities = devicetable.Devicetable.query.all()
    devices = len(dev_entities)*[None]
    for i in range(len(dev_entities)):
        devices[i] = dev_entities[i].to_dict()
    bus_entities = business.Business.query.all()
    businesses = len(bus_entities)*[None]
    for i in range(len(bus_entities)):
        businesses[i] = bus_entities[i].to_dict()
    que_entities = queue.Queue.query.all()
    queues = len(que_entities)*[None]
    for i in range(len(que_entities)):
        queues[i] = que_entities[i].to_dict()
    chas_entities = Chassis.Chassis.query.all()
    chassises = len(chas_entities)*[None]
    for i in range(len(chas_entities)):
        chassises[i] = chas_entities[i].to_dict()
    devicesdata = {'devices': devices, 'businesses': businesses, 'queues': queues, 'chassises': chassises}
    return jsonify(devicesdata)

@app.route('/noviga/devicetables', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin')
def get_all_devices():
    entities = devicetable.Devicetable.query.all()
    return json.dumps([entity.to_dict() for entity in entities])

@app.route('/noviga/devicetables/<int:id>', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin')
def get_device(id):
    entity = devicetable.Devicetable.query.get(id)
    if not entity:
        abort(404)
    return jsonify(entity.to_dict())

@app.route('/noviga/devicetables', methods = ['POST'])
@access.log_required1
@access.requires_roles('Admin')
def create_device():
    if not (request.json['queueId'] and request.json['niChassisId'] and request.json['firmwarename']):
        abort (404)
    entity = devicetable.Devicetable(firmwarename = request.json['firmwarename'])
    chassi = Chassis.Chassis.query.get(request.json['niChassisId'])
    print dir(chassi)
    if not chassi:
        abort(404)
    que = queue.Queue.query.get(request.json['queueId'])
    if not que:
        abort(404)
    biness = business.Business.query.get(que.businessId)
    que.devices.append(entity)
    biness.devices.append(entity)
    chassi.devices.append(entity)
    db.session.add(entity)
    db.session.add(biness)
    db.session.add(chassi)
    db.session.add(que)
    db.session.commit()
    return jsonify(entity.to_dict()), 201

@app.route('/noviga/devicetables/<int:id>', methods = ['PUT'])
@access.log_required1
@access.requires_roles('Admin')
def update_device(id):
    entity = devicetable.Devicetable.query.get(id)
    if not entity:
        abort(404)
    if not (request.json['queueId'] and request.json['niChassisId'] and request.json['firmwarename']):
        abort (404)
    entity.firmwarename = request.json['firmwarename']
    que = queue.Queue.query.get(request.json['queueId'])
    if not que:
        abort(404)
    biness = business.Business.query.get(que.businessId)
    chassi = Chassis.Chassis.query.get(request.json['niChassisId'])
    if not chassi:
        abort(404)
    que.devices.append(entity)
    biness.devices.append(entity)
    chassi.devices.append(entity)
    db.session.add(que)
    db.session.add(biness)
    db.session.add(chassi)
    db.session.commit()
    return jsonify(entity.to_dict()), 200

@app.route('/noviga/devicetables/<int:id>', methods = ['DELETE'])
@access.log_required1
@access.requires_roles('Admin')
def delete_device(id):
    entity = devicetable.Devicetable.query.get(id)
    if not entity:
        abort(404)
    db.session.delete(entity)
    db.session.commit()
    return '', 204


@app.route('/noviga/businesses/<int:businessId>/devicetables', methods = ['GET'])
@access.log_required1
@access.business_check
def get_biness_devices(businessId):
    entities = devicetable.Devicetable.query.filter(devicetable.Devicetable.businessId == businessId).all()
    return json.dumps([entity.to_dict() for entity in entities])
