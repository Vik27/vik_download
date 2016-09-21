from app import app, db
from app.models import business, queue
from flask import abort, jsonify, request
import datetime
import json
from app.functionss import access


@app.route('/noviga/queues/all', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin')
def get_queuesdata():
    bus_entities = business.Business.query.all()
    businesses = len(bus_entities)*[None]
    for i in range(len(bus_entities)):
        businesses[i] = bus_entities[i].to_dict()
    que_entities = queue.Queue.query.all()
    queues = len(que_entities)*[None]
    for i in range(len(que_entities)):
        queues[i] = que_entities[i].to_dict()
    queuesdata = {'businesses': businesses, 'queues': queues}
    return jsonify(queuesdata)

@app.route('/noviga/queues', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin')
def get_all_queues():
    entities = queue.Queue.query.all()
    return json.dumps([entity.to_dict() for entity in entities])

@app.route('/noviga/queues/<int:id>', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin')
def get_queue(id):
    entity = queue.Queue.query.get(id)
    if not entity:
        abort(404)
    return jsonify(entity.to_dict())

@app.route('/noviga/queues', methods = ['POST'])
@access.log_required1
@access.requires_roles('Admin')
def create_queue():
    if not (request.json['businessId'] and request.json['queuename']):
        abort (404)
    entity = queue.Queue(queuename = request.json['queuename'])
    biness = business.Business.query.get(request.json['businessId'])
    if not biness:
        abort(404)
    biness.queues.append(entity)
    db.session.add(biness)
    db.session.commit()
    return jsonify(entity.to_dict()), 201

@app.route('/noviga/queues/<int:id>', methods = ['PUT'])
@access.log_required1
@access.requires_roles('Admin')
def update_queue(id):
    entity = queue.Queue.query.get(id)
    if not entity:
        abort(404)
    if not (request.json['businessId'] and request.json['queuename']):
        abort (404)
    entity.queuename = request.json['queuename']
    biness = business.Business.query.get(request.json['businessId'])
    if not biness:
        abort(404)
    biness.queues.append(entity)
    db.session.add(biness)
    db.session.commit()
    return jsonify(entity.to_dict()), 200

@app.route('/noviga/queues/<int:id>', methods = ['DELETE'])
@access.log_required1
@access.requires_roles('Admin')
def delete_queue(id):
    entity = queue.Queue.query.get(id)
    if not entity:
        abort(404)
    db.session.delete(entity)
    db.session.commit()
    return '', 204


@app.route('/noviga/businesses/<int:businessId>/queues', methods = ['GET'])
@access.log_required1
@access.business_check
def get_biness_queues(businessId):
    entities = queue.Queue.query.filter(queue.Queue.businessId == businessId).all()
    return json.dumps([entity.to_dict() for entity in entities])
