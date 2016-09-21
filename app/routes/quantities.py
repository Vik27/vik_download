from app import app, db
from app.models import quantity
from app.models import unit
from flask import abort, jsonify, request
import datetime
import json
from app.functionss import access

@app.route('/noviga/quantities/all', methods = ['GET'])
@access.log_required1
def get_quantitydata():
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
    quantitydata = {'quantities': quantities, 'units': units}
    return jsonify(quantitydata)


@app.route('/noviga/quantities', methods = ['GET'])
@access.log_required1
def get_all_quantities():
    entities = quantity.Quantity.query.all()
    quantities = len(entities)*[None]
    for i in range(len(entities)):
        quantities[i] = entities[i].to_dict()
        units = unit.Unit.query.filter(unit.Unit.quantityID == entities[i].id).all()
        quantities[i]["units"] = len(units)*[None]
        for ii in range(len(units)):
            quantities[i]["units"][ii] = units[ii].to_dict()
    return json.dumps(quantities)

@app.route('/noviga/quantities/<int:id>', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin')
def get_quantity(id):
    entity = quantity.Quantity.query.get(id)
    if not entity:
        abort(404)
    quant = entity.to_dict()
    units = unit.Unit.query.filter(unit.Unit.quantityID == entity.id).all()
    quant["units"] = len(units)*[None]
    for i in range(len(units)):
        quant["units"][i] = units[i].to_dict()
    return jsonify(quant)

@app.route('/noviga/quantities', methods = ['POST'])
@access.log_required1
@access.requires_roles('Admin')
def create_quantity():
    entity = quantity.Quantity(
        name = request.json['name']
    )
    if (request.json['units']):
        units = unit.Unit.query.filter\
        (unit.Unit.id.in_(request.json['units'])).all()
        for uni in units:
            entity.unitId.append(uni)
            db.session.add(entity)
    else:
        db.session.add(entity)
    db.session.commit()
    quant = entity.to_dict()
    units = unit.Unit.query.filter(unit.Unit.quantityID == entity.id).all()
    quant["units"] = len(units)*[None]
    for i in range(len(units)):
        quant["units"][i] = units[i].to_dict()
    return jsonify(quant), 201

@app.route('/noviga/quantities/<int:id>', methods = ['PUT'])
@access.log_required1
@access.requires_roles('Admin')
def update_quantity(id):
    entity = quantity.Quantity.query.get(id)
    if not entity:
        abort(404)
    entity.name = request.json['name']
    if (request.json['units']):
        if not (set(request.json['units']) == set([x.id for x in unit.Unit.query.filter(unit.Unit.quantityID == id).all()])):
            removeunits = unit.Unit.query.filter((unit.Unit.quantityID == id) & (unit.Unit.id.notin_(request.json['units']))).all()
            for i in range(len(removeunits)):
                entity.unitId.remove(removeunits[i])
            currentunitids = [x.id for x in unit.Unit.query.filter(unit.Unit.quantityID == id).all()]
            addunits = unit.Unit.query.filter((unit.Unit.id.in_(request.json['units'])) &\
            (unit.Unit.id.notin_(currentunitids))).all()
            for ii in range(len(addunits)):
                entity.unitId.append(addunits[ii])
            db.session.add(entity)
    else:
        db.session.add(entity)
    db.session.commit()
    quant = entity.to_dict()
    units = unit.Unit.query.filter(unit.Unit.quantityID == entity.id).all()
    quant["units"] = len(units)*[None]
    for i in range(len(units)):
        quant["units"][i] = units[i].to_dict()
    return jsonify(quant), 200

@app.route('/noviga/quantities/<int:id>', methods = ['DELETE'])
@access.log_required1
@access.requires_roles('Admin')
def delete_quantity(id):
    entity = quantity.Quantity.query.get(id)
    if not entity:
        abort(404)
    entity.modules = []
    db.session.commit()
    db.session.delete(entity)
    db.session.commit()
    return '', 204
