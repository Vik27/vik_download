from app import db

channelnumbertemplate=db.Table('channelnumbertemplate',                            
 
                             db.Column('channelsetupId', db.Integer,db.ForeignKey('channelsetup.id'), nullable=False),
                             db.Column('hwchaschanmapId',db.Integer,db.ForeignKey('hwchaschanmap.id'),nullable=False),
                             db.PrimaryKeyConstraint('channelsetupId', 'hwchaschanmapId') )
