from app import db

modquanmap=db.Table('modquanmap',                            
 
                             db.Column('moduleID', db.Integer,db.ForeignKey('module.id'), nullable=False),
                             db.Column('quantityID',db.Integer,db.ForeignKey('quantity.id'),nullable=False),
                             db.PrimaryKeyConstraint('moduleID', 'quantityID') )
