from app import app, db
from app.models import unit
from flask import abort, jsonify, request
import datetime
import json

@app.route('/noviga/units', methods = ['GET'])
def get_all_units():
    entities = unit.Unit.query.all()
    return json.dumps([entity.to_dict() for entity in entities])

@app.route('/noviga/units/<int:id>', methods = ['GET'])
def get_unit(id):
    entity = unit.Unit.query.get(id)
    if not entity:
        abort(404)
    return jsonify(entity.to_dict())

@app.route('/noviga/units', methods = ['POST'])
def create_unit():
    entity = unit.Unit(
        name = request.json['name']
    )
    db.session.add(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 201

@app.route('/noviga/units/<int:id>', methods = ['PUT'])
def update_unit(id):
    entity = unit.Unit.query.get(id)
    if not entity:
        abort(404)
    entity = unit.Unit(
        name = request.json['name'],
        id = id
    )
    db.session.merge(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 200

@app.route('/noviga/units/<int:id>', methods = ['DELETE'])
def delete_unit(id):
    entity = unit.Unit.query.get(id)
    if not entity:
        abort(404)
    db.session.delete(entity)
    db.session.commit()
    return '', 204
