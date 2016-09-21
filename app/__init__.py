# app/__init__.py

from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy, event, before_models_committed, models_committed
from app.config import BaseConfig
from flask.ext.login import LoginManager
from sqlalchemy import and_
from sqlalchemy.orm import relationship, class_mapper, backref


app = Flask(__name__)
app.config.from_object(BaseConfig)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
session = db.session()
# @event.listens_for(session, 'before_commit')
@before_models_committed.connect_via(app)
def receive_before_commit(sender, changes):
    # self._logger.debug("before_commit: %s", session)
    print sender
    print 'Hello'
    print len(changes)
    for d,typ in changes:
    	print [d.__tablename__,typ]
        # self._logger.info("before_commit >> add: %s", d)
        if typ == 'insert':
            if hasattr(d, 'create_activitylog'):
            	if hasattr(d, 'businessId'):
            		bid = d.businessId
            		unid = d.unitId
            		print "bid::::" + str(bid)
            		print "unid::::" + str(unid)
            		log = d.create_activitylog('update')
            	else:
            		log = d.create_activitylog('create')
        # self._logger.info("before_commit >> mod: %s", d)
        elif typ == 'update':
            if hasattr(d, 'create_activitylog'):
                log = d.create_activitylog('update')
        # self._logger.info("before_commit >> del: %s", d)
        else:
            if hasattr(d, 'create_activitylog'):
                log = d.create_activitylog('delete')
# def receive_before_commit(session):
#     # self._logger.debug("before_commit: %s", session)
#     print 'Hello'
#     for d in session.new:
#         # self._logger.info("before_commit >> add: %s", d)
#         if hasattr(d, 'create_activitylog'):
#             log = d.create_activitylog('create')
#     for d in session.dirty:
#         # self._logger.info("before_commit >> mod: %s", d)
#         if hasattr(d, 'create_activitylog'):
#             log = d.create_activitylog('update')
#     for d in session.deleted:
#         # self._logger.info("before_commit >> del: %s", d)
#         if hasattr(d, 'create_activitylog'):
#             log = d.create_activitylog('delete')

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


from app.models import user
from app.models import business

from app.models import Chassis
from app.models import Module
from app.models import hardwareSetup
from app.models import hwchassismap
from app.models import hwchaschanmap
from app.models import channelsetup
from app.models import quantity
from app.models import unit
from app.models import devicetable
from app.models import project
from app.models import modquanmap
from app.models import queue
from app.models import acquisition
# from app.models import channelnumbertemplate
from app.models import component
from app.models import rawdata
from app.models import livecomponent
from app.models import rawdatasetting
from app.models import serversynclog
from app.models import localsynclog
from app.models import dusratable


from app.routes import index
from app.routes import authentication
from app.routes import users
from app.routes import businesses
from app.routes import Chassis
from app.routes import Modules
from app.routes import devicetables
from app.routes import hardwaresetups
# from app.routes import hwchassismaps
from app.routes import hwchaschanmaps
from app.routes import channelsetups
from app.routes import quantities
from app.routes import units
from app.routes import projects
from app.routes import queues
from app.routes import acquisitions
from app.routes import rabmsgToClient

from app.functionss import access
from app.functionss import acqsettings_check
from app.functionss import hardware_status_check
from app.functionss import project_status_check

ActivityLog=serversynclog.Serversynclog
def auditable(cls, name):
    def create_activitylog(self, activity_type):
    	if hasattr(self, 'businessId'):
    		print 'Yay'
    		bid = self.businessId
    		print bid
    		iid = self.id
    		print iid
    	else:
    		bid = None
        log = ActivityLog(
                          type=activity_type,
                          tablename=table.name,
                          rowid = self.id,
                          idtype = 'global',
                          bid = bid,
                          )
        getattr(self, name).append(log)
        return log

    mapper = class_mapper(cls)
    table = mapper.local_table
    #fkys =  list(table.c.businessId.foreign_keys)[0].column.table
    #print fkys
    cls.create_activitylog = create_activitylog

    # def _get_activitylog(self):
    #     return Session.object_session(self).query(ActivityLog).with_parent(self).all()
    # setattr(cls, '%s_readonly' %(name,), property(_get_activitylog))

    # no constraints, therefore define constraints in an ad-hoc fashion.
    primaryjoin = and_(
            list(table.primary_key)[0] == ActivityLog.__table__.c.rowid,
            ActivityLog.__table__.c.tablename == table.name
    )
    foreign_keys = [ActivityLog.__table__.c.rowid]
    mapper.add_property(name, 
            # @note: because we use the relationship, by default all previous
            # ActivityLog items will be loaded for an object when new one is
            # added. To avoid this, use either dynamic_loader (http://www.sqlalchemy.org/docs/reference/orm/mapping.html#sqlalchemy.orm.dynamic_loader)
            # or lazy='noload'. This is the trade-off decision to be made.
            # Additional benefit of using lazy='noload' is that one can also
            # record DEL operations in the same way as ADD, MOD
            relationship(
                ActivityLog,
                lazy='noload',  # important for relationship
                primaryjoin=primaryjoin, 
                foreign_keys=foreign_keys,
                passive_deletes = True,
                backref=backref('_backref_%s' % table.name, 
                    primaryjoin=list(table.primary_key)[0] == ActivityLog.__table__.c.rowid, 
                    foreign_keys=foreign_keys)
        )
    )

auditable(channelsetup.Channelsetup, 'serversynclogs')