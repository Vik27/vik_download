from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, SmallInteger, String, DateTime, ForeignKey, Table, UnicodeText, Unicode, and_
from sqlalchemy.orm import relationship, dynamic_loader, scoped_session, sessionmaker, class_mapper, backref
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.interfaces import SessionExtension

import logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger()

ACTIVITY_ADD = 1
ACTIVITY_MOD = 2
ACTIVITY_DEL = 3

class ActivityLogSessionExtension(SessionExtension):
    _logger = logging.getLogger('ActivityLogSessionExtension')

    def before_commit(self, session):
        self._logger.debug("before_commit: %s", session)
        for d in session.new:
            self._logger.info("before_commit >> add: %s", d)
            if hasattr(d, 'create_activitylog'):
                log = d.create_activitylog(ACTIVITY_ADD)
        for d in session.dirty:
            self._logger.info("before_commit >> mod: %s", d)
            if hasattr(d, 'create_activitylog'):
                log = d.create_activitylog(ACTIVITY_MOD)
        for d in session.deleted:
            self._logger.info("before_commit >> del: %s", d)
            if hasattr(d, 'create_activitylog'):
                log = d.create_activitylog(ACTIVITY_DEL)


# Configure test data SA
engine = create_engine('sqlite:///:memory:', echo=False)
session = scoped_session(sessionmaker(bind=engine, autoflush=False, extension=ActivityLogSessionExtension()))
Base = declarative_base()
Base.query = session.query_property()

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




class ActivityLog(Base, _BaseMixin):
    __tablename__ = u'activitylog'
    id = Column(Integer, primary_key=True)

    activity_type = Column(SmallInteger, nullable=False)

    target_table = Column(Unicode(20), nullable=False)
    target_id = Column(Integer, nullable=False)
    #target_title = Column(Unicode(255), nullable=False)
    # backref relation for auditable
    target = property(lambda self: getattr(self, '_backref_%s' % self.target_table))


def auditable(cls, name):
    def create_activitylog(self, activity_type):
        log = ActivityLog(
                          activity_type=activity_type,
                          target_table=table.name, 
                          target_title=self.title,
                          )
        getattr(self, name).append(log)
        return log

    mapper = class_mapper(cls)
    table = mapper.local_table
    cls.create_activitylog = create_activitylog

    def _get_activitylog(self):
        return Session.object_session(self).query(ActivityLog).with_parent(self).all()
    setattr(cls, '%s_readonly' %(name,), property(_get_activitylog))

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
                backref=backref('_backref_%s' % table.name, 
                    primaryjoin=list(table.primary_key)[0] == ActivityLog.__table__.c.target_id, 
                    foreign_keys=foreign_keys)
        )
    )

# this will define which classes support the ActivityLog interface
auditable(Document, 'activitylogs')
auditable(Folder, 'activitylogs')

# create db schema
Base.metadata.create_all(engine