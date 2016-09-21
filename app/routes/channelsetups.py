from app import app, db
from app.models import channelsetup, quantity, unit, Module, business, serversynclog
from flask import abort, jsonify, request
import datetime
import json
from app.functionss import access

@app.route('/noviga/channeltemplates/<int:id>', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin')
def get_channeltemplates(id):
    module = Module.Module.query.get(id)
    modulequantIds = [x.id for x in module.quants.all()]
    unitIds = [x.id for x in unit.Unit.query.filter(unit.Unit.quantityID.in_(modulequantIds)).all()]
    entities = channelsetup.Channelsetup.query.filter(channelsetup.Channelsetup.unitId.in_(unitIds)).all()
    chansetups = len(entities)*[None]
    for i in range(len(entities)):
        chansetups[i] = entities[i].to_dict()
        chansetups[i]["quantityId"] = \
        (unit.Unit.query.filter(unit.Unit.id==chansetups[i]["unitId"]).first().to_dict())["quantityID"]
    return json.dumps(chansetups)


@app.route('/noviga/businesses/<int:businessId>/channeltemplates/<int:id>', methods = ['GET'])
@access.log_required1
@access.business_check
def get_biness_channeltemplates(businessId,id):
    module = Module.Module.query.get(id)
    modulequantIds = [x.id for x in module.quants.all()]
    unitIds = [x.id for x in unit.Unit.query.filter(unit.Unit.quantityID.in_(modulequantIds)).all()]
    entities = channelsetup.Channelsetup.query.filter\
    ((channelsetup.Channelsetup.unitId.in_(unitIds)) & (channelsetup.Channelsetup.businessId == businessId)).all()
    chansetups = len(entities)*[None]
    for i in range(len(entities)):
        chansetups[i] = entities[i].to_dict()
        chansetups[i]["quantityId"] = \
        (unit.Unit.query.filter(unit.Unit.id==chansetups[i]["unitId"]).first().to_dict())["quantityID"]
    return json.dumps(chansetups)


@app.route('/noviga/channelsetups', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin')
def get_all_channelsetups():
    entities = channelsetup.Channelsetup.query.all()
    chansetups = len(entities)*[None]
    for i in range(len(entities)):
        chansetups[i] = entities[i].to_dict()
        chansetups[i]["quantityId"] = \
        (unit.Unit.query.filter(unit.Unit.id==chansetups[i]["unitId"]).first().to_dict())["quantityID"]
    return json.dumps(chansetups)


@app.route('/noviga/businesses/<int:businessId>/channelsetups', methods = ['GET'])
@access.log_required1
@access.business_check
def get_biness_channelsetups(businessId):
    entities = channelsetup.Channelsetup.query.filter(channelsetup.Channelsetup.businessId == businessId).all()
    chansetups = len(entities)*[None]
    for i in range(len(entities)):
        chansetups[i] = entities[i].to_dict()
        chansetups[i]["quantityId"] = \
        (unit.Unit.query.filter(unit.Unit.id==chansetups[i]["unitId"]).first().to_dict())["quantityID"]
    return json.dumps(chansetups)


@app.route('/noviga/businesses/<int:businessId>/channelsetups/<int:id>', methods = ['GET'])
@access.log_required1
@access.business_check
def get_biness_channelsetup(businessId,id):
    entity = channelsetup.Channelsetup.query.get(id)
    if not entity:
        abort(404)
    if not (entity.businessId == businessId):
        abort(404)
    chansetup = entity.to_dict()
    chansetup["quantityId"] = \
    (unit.Unit.query.filter(unit.Unit.id==chansetup["unitId"]).first().to_dict())["quantityID"]
    return jsonify(chansetup)

@app.route('/noviga/businesses/<int:businessId>/channelsetups', methods = ['POST'])
@access.log_required1
@access.business_check
def create_biness_channelsetup(businessId):
    biness = business.Business.query.get(businessId)
    if not (request.json['quantityId'] and request.json['unitId']):
        abort(404)
    quant = quantity.Quantity.query.get(request.json['quantityId'])
    if not quant:
        abort(404)
    if not (request.json['name']):
        abort(404)
    measuringunit = unit.Unit.query.filter\
    ((unit.Unit.id==request.json['unitId']) & (unit.Unit.quantityID==request.json['quantityId'])).first()
    if not measuringunit:
        abort(404)
    entity = channelsetup.Channelsetup(
        name = request.json['name']
        , sensitivity = request.json['sensitivity']
    )
    measuringunit.channels.append(entity)
    biness.channeltemplates.append(entity)
    db.session.add(measuringunit)
    db.session.add(biness)
    db.session.commit()

    ##########################
    ##insert in serverlog and dusratable
    ##check if same row already exists in serverlog,
    ## filename 
    chansetup = entity.to_dict()

    # log=serversynclog.Serversynclog(
    #     bid = businessId
    #     , tablename = 'channelsetup'
    #     , rowid = chansetup["id"]
    #     , type = 'create'
    #     , idtype='global'
    #     ,filename =''
    # )

    # logx=serversynclog.Serversynclog.query.filter\
    #     (serversynclog.Serversynclog.tablename==log.tablename).filter\
    #     (serversynclog.Serversynclog.rowid==log.rowid).filter\
    #     (serversynclog.Serversynclog.bid==log.bid).first()


    # if not logx

    # stmt2="""select * from """+log.tablename + """ where id="""+ str(row['rowid'])
    # tlogs=engine.execute(stmt2)
    # ent2=dict(tlogs.items())
    # dusralog=dusratable.Dusratable(
    #     rowValue=json.dumps(ent2))

    # db.session.add(log)
    # db.session.add(dusralog)
    # db.session.commit()


    # ##commit in serverlog and dusratable
    # ##########################



    chansetup["quantityId"] = \
    (unit.Unit.query.filter(unit.Unit.id==chansetup["unitId"]).first().to_dict())["quantityID"]
    return jsonify(chansetup), 201

@app.route('/noviga/businesses/<int:businessId>/channelsetups/<int:id>', methods = ['PUT'])
@access.log_required1
@access.business_check
def update_biness_channelsetup(businessId,id):
    if not (request.json['quantityId'] and request.json['unitId']):
        abort(404)
    quant = quantity.Quantity.query.get(request.json['quantityId'])
    if not quant:
        abort(404)
    measuringunit = unit.Unit.query.filter\
    ((unit.Unit.id==request.json['unitId']) & (unit.Unit.quantityID==request.json['quantityId'])).first()
    if not measuringunit:
        abort(404)
    entity = channelsetup.Channelsetup.query.get(id)
    if not entity:
        abort(404)
    if not (entity.businessId == businessId):
        abort(404)
    entity.name = request.json['name']
    entity.sensitivity = request.json['sensitivity']
    measuringunit.channels.append(entity)
    db.session.add(measuringunit)
    db.session.commit()
    chansetup = entity.to_dict()
    
    # log=serversynclog.Serversynclog(
    #     bid = businessId
    #     , tablename = 'channelsetup'
    #     , rowid = chansetup["id"]
    #     , type = 'update'
    # )

    # db.session.add(log)
    # db.session.commit()    
    chansetup["quantityId"] = \
    (unit.Unit.query.filter(unit.Unit.id==chansetup["unitId"]).first().to_dict())["quantityID"]
    return jsonify(chansetup), 200

@app.route('/noviga/businesses/<int:businessId>/channelsetups/<int:id>', methods = ['DELETE'])
@access.log_required1
@access.business_check
def delete_biness_channelsetup(businessId,id):
    entity = channelsetup.Channelsetup.query.get(id)
    if not entity:
        abort(404)
    if not (entity.businessId == businessId):
        abort(404)
    db.session.delete(entity)
    db.session.commit()

    # log=serversynclog.Serversynclog(
    #     bid = businessId
    #     , tablename = 'channelsetup'
    #     , rowid = id
    #     , type = 'delete'
    # )

    # db.session.add(log)
    # db.session.commit()
    return '', 204

@app.route('/noviga/businesses/<int:businessId>/chansetupsdata', methods = ['GET'])
@access.log_required1
@access.business_check
def get_biness_chansetupsdata(businessId):
    chan_entities = channelsetup.Channelsetup.query.filter(channelsetup.Channelsetup.businessId == businessId).all()
    chansetups = len(chan_entities)*[None]
    for i in range(len(chan_entities)):
        chansetups[i] = chan_entities[i].to_dict()
        chansetups[i]["quantityId"] = \
        (unit.Unit.query.filter(unit.Unit.id==chansetups[i]["unitId"]).first().to_dict())["quantityID"]
    quant_entities = quantity.Quantity.query.all()
    quantities = len(quant_entities)*[None]
    for i in range(len(quant_entities)):
        quantities[i] = quant_entities[i].to_dict()
        units = unit.Unit.query.filter(unit.Unit.quantityID == quant_entities[i].id).all()
        quantities[i]["units"] = len(units)*[None]
        for ii in range(len(units)):
            quantities[i]["units"][ii] = units[ii].to_dict()
    chansetupsdata = {'chansetups': chansetups, 'quantities': quantities}
    return jsonify(chansetupsdata)

@app.route('/noviga/businesses/all/chansetupsdata', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin')
def get_allbiness_chansetupsdata():
    chan_entities = channelsetup.Channelsetup.query.all()
    chansetups = len(chan_entities)*[None]
    for i in range(len(chan_entities)):
        chansetups[i] = chan_entities[i].to_dict()
        chansetups[i]["quantityId"] = \
        (unit.Unit.query.filter(unit.Unit.id==chansetups[i]["unitId"]).first().to_dict())["quantityID"]
    quant_entities = quantity.Quantity.query.all()
    quantities = len(quant_entities)*[None]
    for i in range(len(quant_entities)):
        quantities[i] = quant_entities[i].to_dict()
        units = unit.Unit.query.filter(unit.Unit.quantityID == quant_entities[i].id).all()
        quantities[i]["units"] = len(units)*[None]
        for ii in range(len(units)):
            quantities[i]["units"][ii] = units[ii].to_dict()
    bus_entities = business.Business.query.all()
    businesses = len(bus_entities)*[None]
    for i in range(len(bus_entities)):
        businesses[i] = bus_entities[i].to_dict()
    chansetupsdata = {'chansetups': chansetups, 'quantities': quantities, 'businesses': businesses}
    return jsonify(chansetupsdata)