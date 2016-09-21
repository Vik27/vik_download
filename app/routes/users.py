from app import app, db, bcrypt
from app.models import user
from app.models import business
from flask import abort, jsonify, request
import datetime
import json
from app.functionss import access

class BadRequestError(ValueError):
    pass

def bad_request(message):
    response = jsonify({'message': message})
    response.status_code = 400
    return response

@app.errorhandler(BadRequestError)
def bad_request_handler(error):
    return bad_request(error.message)


@app.route('/noviga/users/all', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin')
def get_usersdata():
    user_entities = user.User.query.all()
    users = len(user_entities)*[None]
    for i in range(len(user_entities)):
        users[i] = user_entities[i].to_dict()
    bus_entities = business.Business.query.all()
    businesses = len(bus_entities)*[None]
    for i in range(len(bus_entities)):
        businesses[i] = bus_entities[i].to_dict()
    usersdata = {'users': users, 'businesses': businesses}
    return jsonify(usersdata)


@app.route('/noviga/users', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin')
def get_all_users():
    entities = user.User.query.all()
    return json.dumps([entity.to_dict() for entity in entities])

@app.route('/noviga/users', methods = ['POST'])
@access.log_required1
@access.requires_roles('Admin')
def create_user():
    entity = user.User(
        username = request.json['username']
        , password = request.json['password']
        , contact_email = request.json['contact_email']
        , role = request.json['role']
    )
    if (request.json['businessId']):
        binessUsers = user.User.query.filter(user.User.businessId==request.json['businessId']).all()
        biness = business.Business.query.get(request.json['businessId'])
        if not biness:
            abort(404)
        if (len(binessUsers) < biness.allowedUsers):
            biness.users.append(entity)
            db.session.add(biness)
            db.session.commit()
        else:
            raise BadRequestError('Allowed Users limit reached.')
    else:
        db.session.add(entity)
        db.session.commit()
    return jsonify(entity.to_dict()), 201

@app.route('/noviga/users/<int:id>', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin')
def get_user(id):
    entity = user.User.query.get(id)
    if not entity:
        abort(404)
    return jsonify(entity.to_dict())

@app.route('/noviga/users/<int:id>', methods = ['PUT'])
@access.log_required1
@access.requires_roles('Admin')
def update_user(id):
    entity = user.User.query.get(id)
    if not entity:
        abort(404)
    entity.username = request.json['username']
    entity.password = bcrypt.generate_password_hash(request.json['password'])
    entity.contact_email = request.json['contact_email']
    entity.role = request.json['role']

    if (request.json['businessId']):
        if (entity.businessId == request.json['businessId']):
            db.session.commit()
        else:
            requestedbiness = business.Business.query.get(request.json['businessId'])
            currentbinessUsers = len(user.User.query.filter(user.User.businessId==request.json['businessId']).all())
            if (currentbinessUsers < requestedbiness.allowedUsers):
                requestedbiness.users.append(entity)
                db.session.add(requestedbiness)
                db.session.commit()
                entity = user.User.query.get(id)
            else:
                db.session.commit()
                raise BadRequestError('Cannot change Business. Requested business\'s allowed Users limit reached.')
    else:
        db.session.commit()
    return jsonify(entity.to_dict()), 200

@app.route('/noviga/users/<int:id>', methods = ['DELETE'])
@access.log_required1
@access.requires_roles('Admin')
def delete_user(id):
    entity = user.User.query.get(id)
    if not entity:
        abort(404)
    db.session.delete(entity)
    db.session.commit()
    return '', 204


@app.route('/noviga/businesses/<int:businessId>/users/<int:userId>', methods = ['GET'])
@access.log_required1
def get_biness_user(businessId,userId):
    entity = user.User.query.filter(user.User.businessId==businessId)\
        .filter(user.User.id==userId).all()
    if not entity:
        abort(404)
    return jsonify(entity.to_dict())

@app.route('/noviga/businesses/<int:businessId>/users', methods = ['GET'])
@access.log_required1
@access.requires_roles('Admin','Manager')
def get_biness_all_users(businessId):
    biness = business.Business.query.get(businessId)
    if not biness:
        abort(404)
    entities = user.User.query.filter(user.User.businessId==businessId).all()
    return json.dumps([entity.to_dict() for entity in entities])

@app.route('/noviga/businesses/<int:businessId>/users', methods = ['POST'])
@access.log_required1
@access.requires_roles('Admin','Manager')
def create_biness_user(businessId):
    biness = business.Business.query.get(businessId)
    if not biness:
        abort(404)
    binessUsers = user.User.query.filter(User.businessId==businessId).all()
    if (len(binessUsers) < biness.allowedUsers):
        entity = user.User(
            username = request.json['username']
            , password = request.json['password']
            , contact_email = request.json['contact_email']
            , role = request.json['role']
        )
        biness.users.append(entity)
        db.session.add(biness)
        db.session.commit()
    else:
        entity = ""
    return jsonify(entity.to_dict()), 201

@app.route('/noviga/businesses/<int:businessId>/users/<int:userId>', methods = ['PUT'])
@access.log_required1
def update_biness_user(businessId,userId):
    entity = user.User.query.filter(User.businessId==businessId)\
        .filter(User.id==userId).all()
    if not entity:
        abort(404)
    entity.username = request.json['username']
    entity.password = request.json['password']
    entity.contact_email = request.json['contact_email']
    entity.role = request.json['role']
    db.session.commit()
    return jsonify(entity.to_dict()), 200

@app.route('/noviga/businesses/<int:businessId>/users/<int:id>', methods = ['DELETE'])
@access.log_required1
@access.requires_roles('Admin','Manager')
def delete_biness_user(id):
    entity = user.User.query.filter(User.businessId==businessId)\
        .filter(User.id==userId).all()
    if not entity:
        abort(404)
    db.session.delete(entity)
    db.session.commit()
    return '', 204
