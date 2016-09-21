from app import app, db
from app.models import project, business, user, hardwareSetup, devicetable
from flask import abort, jsonify, request, g
from datetime import datetime
import json
from app.functionss import access, project_status_check
from app.routes import rabmsgToClient

@app.route('/noviga/projects', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin')
def get_all_projects():
    entities = project.Project.query.all()
    projects = len(entities)*[None]
    for i in range(len(entities)):
        projects[i] = entities[i].to_dict()
        projects[i]['created_on'] = str(entities[i].timestamp)
    return json.dumps(projects)

@app.route('/noviga/projects/<int:id>', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin')
def get_project(id):
    entity = project.Project.query.get(id)
    if not entity:
        abort(404)
    projct = entity.to_dict()
    projct['created_on'] = str(entity.timestamp)
    return jsonify(projct)

@app.route('/noviga/projects', methods = ['POST'])
@access.log_required1
@access.requires_roles('Admin')
def create_project():
    if not (request.json['businessId']):
        abort(404)
    biness = business.Business.query.get(request.json['businessId'])
    if not biness:
        abort(404)
    projectdata = request.json['projectsetup']
    entity = project.Project(
        name = projectdata['name']
        , timestamp = datetime.utcnow()
        , description = projectdata['description']
    )
    biness.projects.append(entity)
    db.session.add(biness)
    currentuser = user.User.query.get(g.user.id)
    currentuser.projects.append(entity)
    db.session.add(currentuser)
    if not ((projectdata['hwsetupId']==None) or (projectdata['hwsetupId']=='None')):
        hwsetup = hardwareSetup.HardwareSetup.query.get(projectdata['hwsetupId'])
        if not hwsetup:
            abort(404)
        regddevbiness = devicetable.Devicetable.query.get(hwsetup.deviceId).businessId
        if not(regddevbiness == biness.id):
            abort(404)
        hwsetup.projects.append(entity)
        db.session.add(hwsetup)
    db.session.add(entity)
    db.session.commit()
    project_status_check.project_check(entity.id)
    prjct = entity.to_dict();


    log=serversynclog.Serversynclog(
        bid = businessId
        , tablename = 'channelsetup'
        , rowid = chansetup["id"]
        , type = 'create'
    )

    db.session.add(log)
    db.session.commit()


    prjct['created_on'] = str(entity.timestamp);
    return jsonify(prjct), 201

@app.route('/noviga/projects/<int:id>', methods = ['PUT'])
@access.log_required1
@access.requires_roles('Admin')
def update_project(id):
    if not (request.json['businessId']):
        abort(404)
    biness = business.Business.query.get(request.json['businessId'])
    if not biness:
        abort(404)
    projectdata = request.json['projectsetup']
    if not projectdata:
        abort(404)
    entity = project.Project.query.get(id)
    if not entity:
        abort(404)
    if not (entity.businessId == biness.id):
        abort(404)
    entity.name = projectdata['name']
    entity.description = projectdata['description']
    if not ((projectdata['hwsetupId']==None) or (projectdata['hwsetupId']=='None')):
        hwsetup = hardwareSetup.HardwareSetup.query.get(projectdata['hwsetupId'])
        if not hwsetup:
            abort(404)
        regddevbiness = devicetable.Devicetable.query.get(hwsetup.deviceId).businessId
        if not(regddevbiness == biness.id):
            abort(404)
        hwsetup.projects.append(entity)
        db.session.add(hwsetup)
    else:
        if (entity.hwsetupId):
            hwsetup = hardwareSetup.HardwareSetup.query.get(entity.hwsetupId)
            hwsetup.projects.remove(entity)
            db.session.add(hwsetup)
    db.session.commit()
    project_status_check.project_check(id)
    prjct = entity.to_dict();
    prjct['created_on'] = str(entity.timestamp);
    return jsonify(prjct), 200

@app.route('/noviga/projects/<int:id>', methods = ['DELETE'])
@access.log_required1
@access.requires_roles('Admin')
def delete_project(id):
    entity = project.Project.query.get(id)
    if not entity:
        abort(404)
    db.session.delete(entity)
    db.session.commit()
    return '', 204


@app.route('/noviga/businesses/<int:businessId>/projects', methods = ['GET'])
@access.log_required1
@access.business_check
def get_biness_projects(businessId):
    entities = project.Project.query.filter(project.Project.businessId == businessId).all()
    projects = len(entities)*[None]
    for i in range(len(entities)):
        projects[i] = entities[i].to_dict()
        projects[i]['created_on'] = str(entities[i].timestamp)
    return json.dumps(projects)


@app.route('/noviga/businesses/<int:businessId>/projects/<int:id>', methods = ['GET'])
@access.log_required1
@access.business_check
def get_biness_project(businessId,id):
    biness = business.Business.query.get(businessId)
    entity = project.Project.query.get(id)
    if not entity:
        abort(404)
    if not(entity.businessId == biness.id):
        abort(404)
    return jsonify(entity.to_dict())


@app.route('/noviga/businesses/<int:businessId>/projects', methods = ['POST'])
@access.log_required1
@access.business_check
def create_biness_project(businessId):
    biness = business.Business.query.get(businessId)
    projectdata = request.json
    if not(projectdata['name']):
        abort(404)
    entity = project.Project(
        name = projectdata['name']
        , timestamp = datetime.utcnow()
        , description = projectdata['description']
    )
    biness.projects.append(entity)
    db.session.add(biness)
    currentuser = user.User.query.get(g.user.id)
    currentuser.projects.append(entity)
    db.session.add(currentuser)
    if not (projectdata['hwsetupId']):
        abort(404)
    if not ((projectdata['hwsetupId']==None) or (projectdata['hwsetupId']=='None')):
        hwsetup = hardwareSetup.HardwareSetup.query.get(projectdata['hwsetupId'])
        if not hwsetup:
            abort(404)
        regddevbiness = devicetable.Devicetable.query.get(hwsetup.deviceId).businessId
        if not(regddevbiness == biness.id):
            abort(404)
        hwsetup.projects.append(entity)
        db.session.add(hwsetup)
    else:
        abort(404)
    db.session.add(entity)
    db.session.commit()
    project_status_check.project_check(entity.id)
    prjct = entity.to_dict();
    prjct['created_on'] = str(entity.timestamp);
    return jsonify(prjct), 201


@app.route('/noviga/businesses/<int:businessId>/projects/<int:id>', methods = ['PUT'])
@access.log_required1
@access.business_check
def update_biness_project(businessId,id):
    biness = business.Business.query.get(businessId)
    projectdata = request.json
    entity = project.Project.query.get(id)
    if not entity:
        abort(404)
    if not (entity.businessId == biness.id):
        abort(404)
    entity.name = projectdata['name']
    entity.description = projectdata['description']
    if not (projectdata['hwsetupId']):
        abort(404)
    if not ((projectdata['hwsetupId']==None) or (projectdata['hwsetupId']=='None')):
        hwsetup = hardwareSetup.HardwareSetup.query.get(projectdata['hwsetupId'])
        if not hwsetup:
            abort(404)
        regddevbiness = devicetable.Devicetable.query.get(hwsetup.deviceId).businessId
        if not(regddevbiness == biness.id):
            abort(404)
        hwsetup.projects.append(entity)
        db.session.add(hwsetup)
    else:
        abort(404)
    db.session.commit()
    project_status_check.project_check(id)
    prjct = entity.to_dict();
    prjct['created_on'] = str(entity.timestamp);
    return jsonify(prjct), 200


@app.route('/noviga/businesses/<int:businessId>/projects/<int:id>', methods = ['DELETE'])
@access.log_required1
@access.business_check
def delete_biness_project(businessId,id):
    biness = business.Business.query.get(businessId)
    entity = project.Project.query.get(id)
    if not entity:
        abort(404)
    if not (entity.businessId == biness.id):
        abort(404)
    db.session.delete(entity)
    db.session.commit()
    return '', 204


@app.route('/noviga/businesses/<int:businessId>/projectsdata', methods = ['GET'])
@access.log_required1
@access.business_check
def get_biness_projectsdata(businessId):
    prj_entities = project.Project.query.filter(project.Project.businessId == businessId).all()
    projects = len(prj_entities)*[None]
    for i in range(len(prj_entities)):
        project_status_check.project_check(prj_entities[i].id)
        projects[i] = prj_entities[i].to_dict()
        projects[i]['created_on'] = str(prj_entities[i].timestamp)
    hw_entities = hardwareSetup.HardwareSetup.query.filter\
    (hardwareSetup.HardwareSetup.deviceId.in_([x.id for x in devicetable.Devicetable.query.filter\
        (devicetable.Devicetable.businessId == businessId).all()])).all()
    hwsetups = len(hw_entities)*[None]
    for i in range(len(hw_entities)):
        hwsetups[i] = hw_entities[i].to_dict()
    projectsdata = {'projects': projects, 'hwsetups': hwsetups}
    return json.dumps(projectsdata)

@app.route('/noviga/businesses/all/projectsdata', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin')
def get_allbiness_projectsdata():

    prj_entities = project.Project.query.all()
    projects = len(prj_entities)*[None]
    for i in range(len(prj_entities)):
        project_status_check.project_check(prj_entities[i].id)
        projects[i] = prj_entities[i].to_dict()
        projects[i]['created_on'] = str(prj_entities[i].timestamp)
    hw_entities = hardwareSetup.HardwareSetup.query.all()
    hwsetups = len(hw_entities)*[None]
    for i in range(len(hw_entities)):
        hwsetups[i] = hw_entities[i].to_dict()
    bus_entities = business.Business.query.all()
    businesses = len(bus_entities)*[None]
    for i in range(len(bus_entities)):
        businesses[i] = bus_entities[i].to_dict()
    dev_entities = devicetable.Devicetable.query.all()
    devices = len(dev_entities)*[None]
    for i in range(len(dev_entities)):
        devices[i] = dev_entities[i].to_dict()
    projectsdata = {'projects': projects, 'hwsetups': hwsetups, 'businesses': businesses, 'devices': devices}
    return jsonify(projectsdata)


@app.route('/noviga/businesses/<int:businessId>/runproject/<int:id>', methods = ['GET'])
@access.log_required1
@access.business_check
def get_biness_runproject(businessId,id):
    print "User requested to start project "+ str(id)
    reply=rabmsgToClient.startProjSet(id)
    print "reply from local after run project request: " + reply
    return jsonify({'runans':reply})


@app.route('/noviga/runproject/<int:id>', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin')
def get_runproject(id):
   print "User requested to start project "+ str(id)
   reply=rabmsgToClient.startProjSet(id)
   print "reply from local after run project request: " + reply
   return jsonify({'runans':reply})

