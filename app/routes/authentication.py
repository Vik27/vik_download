from app import app, db, lm, bcrypt
from app.models.user import User
from flask import abort, jsonify, request, session, g, request, redirect, url_for
import datetime
import json
from app.functionss import access
from flask.ext.login import login_user, logout_user, current_user

@lm.user_loader
def user_loader(userid):
    return User.query.get(int(userid))

@app.before_request
def before_request():
    g.user = current_user
    # return jsonify({'data' : g.user.username})
    # return jsonify({'data' : user})


@app.route('/noviga/login', methods=['POST'])
def login():
    json_data = request.json
    user = User.query.filter_by(username=json_data['username']).first()
    if user and bcrypt.check_password_hash(user.password, json_data['password']):
        login_user(user)
        status = True
    else:
        status = False
    return jsonify({'name': user.username, 'result': status, 'businessId': user.businessId, 'role': user.role})


@app.route('/noviga/logout')
@access.log_required1
def logout():
    logout_user()
    # return redirect(url_for('root'))
    return jsonify({'result': True})

# @app.route('/noviga/dummy')
# def dummy():
#     if session.get('logged_in'):
#         if session['logged_in']:
#             return jsonify({'status': True})
#     else:
#         return jsonify({'status': False})

@app.route('/noviga/getUser')
# @access.log_required1
# @access.requires_roles('Admin')
def getUser():
    loggedInUser = None
    if not g.user.is_anonymous:
        loggedInUser = User.query.filter_by(username=g.user.username).first()
        loggedInUser.password = None
        return jsonify(loggedInUser.to_dict())
    else:
        return json.dumps(loggedInUser)
    # else:
    #     return jsonify({'status': False})

@app.route('/noviga/getStatus')
def getStatus():
    status = False
    if not g.user.is_anonymous:
        status = True
    return jsonify({'status' : status})
    
# @app.route('/noviga/register', methods=['POST'])
# # @access.log_required1
# def register():
#     json_data = request.json
#     user = User(
#         username=json_data['username'],
#         password=json_data['password'],
#         email=json_data['email']
#     )
#     try:
#         db.session.add(user)
#         db.session.commit()
#         status = 'success'
#     except:
#         status = 'this user is already registered'
#     db.session.close()
#     return jsonify({'result': status})

# @app.route('/noviga/dummy1', methods=['POST'])
# def dummy1():
#     pass