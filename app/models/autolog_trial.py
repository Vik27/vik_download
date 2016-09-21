from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, SmallInteger, String, DateTime, ForeignKey, Table, UnicodeText, Unicode, and_, event
from sqlalchemy.orm import relationship, dynamic_loader, scoped_session, sessionmaker, class_mapper, backref, column_property
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.interfaces import SessionExtension

import logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger()

ACTIVITY_ADD = 1
ACTIVITY_MOD = 2
ACTIVITY_DEL = 3

# class ActivityLogSessionExtension(SessionExtension):
#     _logger = logging.getLogger('ActivityLogSessionExtension')

#     def before_commit(self, session):
#         self._logger.debug("before_commit: %s", session)
#         for d in session.new:
#             self._logger.info("before_commit >> add: %s", d)
#             if hasattr(d, 'create_activitylog'):
#                 log = d.create_activitylog(ACTIVITY_ADD)
#         for d in session.dirty:
#             self._logger.info("before_commit >> mod: %s", d)
#             if hasattr(d, 'create_activitylog'):
#                 log = d.create_activitylog(ACTIVITY_MOD)
#         for d in session.deleted:
#             self._logger.info("before_commit >> del: %s", d)
#             if hasattr(d, 'create_activitylog'):
#                 log = d.create_activitylog(ACTIVITY_DEL)


# Configure test data SA
engine = create_engine('mysql://root:qwe123@localhost:3306/autologs', echo=False)
session = scoped_session(sessionmaker(bind=engine, autoflush=False))
Base = declarative_base()
Base.query = session.query_property()

@event.listens_for(session, 'before_commit')
def receive_before_commit(session):
    # self._logger.debug("before_commit: %s", session)
    print 'Hello'
    for d in session.new:
        # self._logger.info("before_commit >> add: %s", d)
        if hasattr(d, 'create_activitylog'):
            log = d.create_activitylog(1)
    for d in session.dirty:
        # self._logger.info("before_commit >> mod: %s", d)
        if hasattr(d, 'create_activitylog'):
            log = d.create_activitylog(2)
    for d in session.deleted:
        # self._logger.info("before_commit >> del: %s", d)
        if hasattr(d, 'create_activitylog'):
            log = d.create_activitylog(3)

class _BaseMixin(object):
    """ Just a helper mixin class to set properties on object creation.  
    Also provides a convenient default __repr__() function, but be aware that 
    also relationships are printed, which might result in loading relations.
    """
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return "<%s(%s)>" % (self.__class__.__name__, 
            ', '.join('%s=%r' % (k, self.__dict__[k]) 
                for k in sorted(self.__dict__) if '_sa_' != k[:4] and '_backref_' != k[:9])
            )

class User(Base, _BaseMixin):
    __tablename__ = u'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))

class Document(Base, _BaseMixin):
    __tablename__ = u'documents'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), nullable=False)
    body = Column(UnicodeText, nullable=False)

class Folder(Base, _BaseMixin):
    __tablename__ = u'folders'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), nullable=False)
    comment = Column(UnicodeText, nullable=False)

class ActivityLog(Base, _BaseMixin):
    __tablename__ = u'activitylog'
    id = Column(Integer, primary_key=True)

    activity_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    activity_by = relationship(User) # @note: no need to specify the primaryjoin
    activity_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    activity_type = Column(SmallInteger, nullable=False)

    target_table = Column(Unicode(20), nullable=False)
    target_id = Column(Integer, nullable=False)
    target_title = Column(Unicode(255), nullable=False)
    # backref relation for auditable
    target = property(lambda self: getattr(self, '_backref_%s' % self.target_table))

def _get_user():
    """ This method returns the User object for the current user.
    @todo: proper implementation required
    @hack: currently returns the 'user2'
    """
    return session.query(User).filter_by(name='user2').one()

# auditable support function
# based on first non-FK version from http://techspot.zzzeek.org/?p=13
def auditable(cls, name):
    def create_activitylog(self, activity_type):
        log = ActivityLog(activity_by=_get_user(),
                          activity_type=activity_type,
                          target_table=table.name, 
                          target_title=self.title,
                          target_id = self.id,
                          )
        getattr(self, name).append(log)
        return log

    mapper = class_mapper(cls)
    table = mapper.local_table
    cls.create_activitylog = create_activitylog

    # def _get_activitylog(self):
    #     return Session.object_session(self).query(ActivityLog).with_parent(self).all()
    # setattr(cls, '%s_readonly' %(name,), property(_get_activitylog))

    # no constraints, therefore define constraints in an ad-hoc fashion.
    primaryjoin = and_(
            list(table.primary_key)[0] == ActivityLog.__table__.c.target_id,
            ActivityLog.__table__.c.target_table == table.name
    )
    foreign_keys = [ActivityLog.__table__.c.target_id]
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
                    primaryjoin=list(table.primary_key)[0] == ActivityLog.__table__.c.target_id, 
                    foreign_keys=foreign_keys)
        )
    )

# this will define which classes support the ActivityLog interface
auditable(Document, 'activitylogs')
auditable(Folder, 'activitylogs')

# create db schema
Base.metadata.create_all(engine)


## >>>>> TESTS >>>>>>

# create some basic data first
u1 = User(name='user1')
u2 = User(name='user2')
session.add(u1)
session.add(u2)
session.commit()
session.expunge_all()
# --check--
assert not(_get_user() is None)


##############################
## ADD
##############################
_logger.info('-' * 80)
d1 = Document(title=u'Document-1', body=u'Doc1 some body skipped the body')
# when not using SessionExtension for any reason, this can be called manually
# d1.create_activitylog(ACTIVITY_ADD)
session.add(d1)
session.commit()

f1 = Folder(title=u'Folder-1', comment=u'This folder is empty')
# when not using SessionExtension for any reason, this can be called manually
# f1.create_activitylog(ACTIVITY_ADD)
session.add(f1)
session.commit()

# --check--
session.expunge_all()
logs = session.query(ActivityLog).all()
_logger.debug(logs)
assert len(logs) == 2
assert logs[0].activity_type == ACTIVITY_ADD
assert logs[0].target.title == u'Document-1'
assert logs[0].target.title == logs[0].target_title
assert logs[1].activity_type == ACTIVITY_ADD
assert logs[1].target.title == u'Folder-1'
assert logs[1].target.title == logs[1].target_title

##############################
## MOD(ify)
##############################
_logger.info('-' * 80)
session.expunge_all()
d1 = session.query(Document).filter_by(id=1).one()
assert d1.title == u'Document-1'
assert d1.body == u'Doc1 some body skipped the body'
assert d1.activitylogs == []
d1.title = u'Modified: Document-1'
d1.body = u'Modified: body'
# when not using SessionExtension (or it does not work, this can be called manually)
# d1.create_activitylog(ACTIVITY_MOD)
session.commit()
# _logger.debug(d1.activitylogs_readonly)

# --check--
session.expunge_all()
logs = session.query(ActivityLog).all()
assert len(logs)==3
assert logs[2].activity_type == ACTIVITY_MOD
assert logs[2].target.title == u'Modified: Document-1'
assert logs[2].target.title == logs[2].target_title


##############################
## DEL(ete)
##############################
_logger.info('-' * 80)
session.expunge_all()
d1 = session.query(Document).filter_by(id=1).one()
# when not using SessionExtension for any reason, this can be called manually,
# d1.create_activitylog(ACTIVITY_DEL)
# session.commit()
session.delete(d1)
session.commit()
session.expunge_all()

# # --check--
# session.expunge_all()
# logs = session.query(ActivityLog).all()
# assert len(logs)==4
# assert logs[0].target is None
# assert logs[2].target is None
# assert logs[3].activity_type == ACTIVITY_DEL
# assert logs[3].target is None

# ##############################
# ## print all activity logs
# ##############################
# _logger.info('=' * 80)
# logs = session.query(ActivityLog).all()
# for log in logs:
#     _ = log.target
#     _logger.info("%s -> %s", log, log.target)

# ##############################
# ## navigate from main object
# ##############################
# _logger.info('=' * 80)
# session.expunge_all()
# f1 = session.query(Folder).filter_by(id=1).one()
# _logger.info(f1.activitylogs_readonly)