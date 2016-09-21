from app import app, db
from app.models import business
from app.models import user
from flask import abort, jsonify, request
import datetime
import json
from app.functionss import access

@app.route('/noviga/businesses', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin')
def get_all_businesses():
    entities = business.Business.query.all()
    binesses = len(entities)*[None]
    for i in range(len(entities)):
        binesses[i] = entities[i].to_dict()
        binesses[i]["currentUsers"] = len(user.User.query.filter\
            (user.User.businessId==binesses[i]["id"]).all())
    return json.dumps(binesses)

@app.route('/noviga/businesses/<int:id>', methods = ['GET'])
@access.log_required1
@access.business_check
def get_business(id):
    entity = business.Business.query.get(id)
    if not entity:
        abort(404)
    return jsonify(entity.to_dict())

@app.route('/noviga/businesses', methods = ['POST'])
@access.log_required1
@access.requires_roles('Admin')
def create_business():
    entity = business.Business(
        name = request.json['name']
        , allowedRunProjects = request.json['allowedRunProjects']
        , allowedUsers = request.json['allowedUsers']
    )
    db.session.add(entity)
    db.session.commit()
    biness = entity.to_dict()
    biness['currentUsers'] = 0
    return jsonify(biness), 201

@app.route('/noviga/businesses/<int:id>', methods = ['PUT'])
@access.log_required1
@access.requires_roles('Admin')
def update_business(id):
    entity = business.Business.query.get(id)
    if not entity:
        abort(404)
    entity = business.Business(
        name = request.json['name']
        , allowedRunProjects = request.json['allowedRunProjects']
        , allowedUsers = request.json['allowedUsers']
        , id = id
    )
    db.session.merge(entity)
    db.session.commit()
    biness = entity.to_dict()
    biness['currentusers'] = len(user.User.query.filter\
            (user.User.businessId==id).all())
    return jsonify(biness), 200

@app.route('/noviga/businesses/<int:id>', methods = ['DELETE'])
@access.log_required1
@access.requires_roles('Admin')
def delete_business(id):
    entity = business.Business.query.get(id)
    if not entity:
        abort(404)
    db.session.delete(entity)
    db.session.commit()
    return '', 204
