from app import app, db
from app.models import Module
from app.models import quantity, unit
from flask import abort, jsonify, request
import datetime
import json
from app.functionss import access

@app.route('/noviga/Modules', methods = ['GET'])
@access.log_required1
def get_all_Modules():
    entities = Module.Module.query.all()
    modules = len(entities)*[None]
    for ii in range(len(entities)):
        modules[ii] = entities[ii].to_dict()
        quantis = entities[ii].quants.all()
        modules[ii]["quantities"] = len(quantis)*[None]
        for iii in range(len(quantis)):
            modules[ii]["quantities"][iii] = quantis[iii].to_dict()
    return json.dumps(modules)

@app.route('/noviga/Modules/<int:id>', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin')
def get_Module(id):
    entity = Module.Module.query.get(id)
    if not entity:
        abort(404)
    module = entity.to_dict()
    quantis = entity.quants.all()
    module["quantities"] = len(quantis)*[None]
    for ii in range(len(quantis)):
        module["quantities"][ii] = quantis[ii].to_dict()
    return jsonify(module)

@app.route('/noviga/Modules', methods = ['POST'])
@access.log_required1
@access.requires_roles('Admin')
def create_Module():
    entity = Module.Module(
        modelNo = request.json['modelNo']
        , maxChannels = request.json['maxChannels']
        , maxSamplingRate = request.json['maxSamplingRate']
        , peakVoltRange = request.json['peakVoltRange']
        , type = request.json['type']
        , daqmxDeviceId = request.json['daqmxDeviceId']
    )
    if (request.json['quantities']):
        quantities = quantity.Quantity.query.filter\
        (quantity.Quantity.id.in_(request.json['quantities'])).all()
        for quant in quantities:
            entity.quantities.append(quant)
        db.session.add(entity)
        db.session.commit()
    else:
        db.session.add(entity)
        db.session.commit()
    module = entity.to_dict()
    quantis = entity.quants.all()
    module["quantities"] = len(quantis)*[None]
    for ii in range(len(quantis)):
        module["quantities"][ii] = quantis[ii].to_dict()
    return jsonify(module), 201

@app.route('/noviga/Modules/<int:id>', methods = ['PUT'])
@access.log_required1
@access.requires_roles('Admin')
def update_Module(id):
    entity = Module.Module.query.get(id)
    if not entity:
        abort(404)
    entity.modelNo = request.json['modelNo']
    entity.maxChannels = request.json['maxChannels']
    entity.maxSamplingRate = request.json['maxSamplingRate']
    entity.peakVoltRange = request.json['peakVoltRange']
    entity.type = request.json['type']
    entity.daqmxDeviceId = request.json['daqmxDeviceId']
    if (request.json['quantities']):
        if not (set(request.json['quantities']) == set([x.id for x in entity.quants.all()])):
            removequants = entity.quants.filter\
            (quantity.Quantity.id.notin_(request.json['quantities'])).all()
            for i in range(len(removequants)):
                entity.quantities.remove(removequants[i])
            currentquantids = [x.id for x in entity.quants.all()]
            addquants = quantity.Quantity.query.filter\
            ((quantity.Quantity.id.in_(request.json['quantities'])) &\
                (quantity.Quantity.id.notin_(currentquantids))).all()
            for ii in range(len(addquants)):
                entity.quantities.append(addquants[ii])
            db.session.add(entity)
    db.session.commit()
    module = entity.to_dict()
    quantis = entity.quants.all()
    module["quantities"] = len(quantis)*[None]
    for ii in range(len(quantis)):
        module["quantities"][ii] = quantis[ii].to_dict()
    return jsonify(module), 200

@app.route('/noviga/Modules/<int:id>', methods = ['DELETE'])
@access.log_required1
@access.requires_roles('Admin')
def delete_Module(id):
    entity = Module.Module.query.get(id)
    if not entity:
        abort(404)
    entity.quantities=[]
    db.session.commit()
    db.session.delete(entity)
    db.session.commit()
    return '', 204


@app.route('/noviga/Modules/all', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin')
def get_Moduledata():
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
    moduledata = {'modules': modules, 'quantities': quantities}
    return jsonify(moduledata)