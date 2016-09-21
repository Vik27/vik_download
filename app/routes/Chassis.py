from app import app, db
from app.models import Chassis
from flask import abort, jsonify, request
import datetime
import json
from app.functionss import access

@app.route('/noviga/Chassis', methods = ['GET'])
@access.log_required1
def get_all_Chassis():
    entities = Chassis.Chassis.query.all()
    return json.dumps([entity.to_dict() for entity in entities])

@app.route('/noviga/Chassis/<int:id>', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin')
def get_Chassis(id):
    entity = Chassis.Chassis.query.get(id)
    if not entity:
        abort(404)
    return jsonify(entity.to_dict())

@app.route('/noviga/Chassis', methods = ['POST'])
@access.log_required1
@access.requires_roles('Admin')
def create_Chassis():
    entity = Chassis.Chassis(
        modelNo = request.json['modelNo']
        , maxSlots = request.json['maxSlots']
        , connectionType = request.json['connectionType']
        , daqmxDeviceId = request.json['daqmxDeviceId']
    )
    db.session.add(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 201

@app.route('/noviga/Chassis/<int:id>', methods = ['PUT'])
@access.log_required1
@access.requires_roles('Admin')
def update_Chassis(id):
    entity = Chassis.Chassis.query.get(id)
    if not entity:
        abort(404)
    entity = Chassis.Chassis(
        modelNo = request.json['modelNo'],
        maxSlots = request.json['maxSlots'],
        connectionType = request.json['connectionType'],
        daqmxDeviceId = request.json['daqmxDeviceId'],
        id = id
    )
    db.session.merge(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 200

@app.route('/noviga/Chassis/<int:id>', methods = ['DELETE'])
@access.log_required1
@access.requires_roles('Admin')
def delete_Chassis(id):
    entity = Chassis.Chassis.query.get(id)
    if not entity:
        abort(404)
    db.session.delete(entity)
    db.session.commit()
    return '', 204
