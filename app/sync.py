from sqlalchemy.dialects.mysql import BLOB
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, DateTime, Enum, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from sqlalchemy.dialects.mysql import BLOB, LONGBLOB


from datetime import datetime
 
import time
import string
import random

Base = declarative_base()
engine = create_engine('mysql://root:qwe123@localhost:3306/logintry')
bid=1
filepath1= "~/syncdata/" + str(bid) + '/log.csv'

#logstmt="select * from serversynclog" + " into outfile " + filepath1 + " FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';"

logs=engine.execute("select * from serversynclog")

for row in logs:
	if row['type']== 'create':
		filepath= "/tmp"  + '/' + row['tablename'] + str(row['bid']) + '.csv'   #"/home/ubuntu/syncdata/" + str(row['bid']) + '/' + 
		print filepath
		stmt= "select * from " + row['tablename'] + " where id =" +str(row['rowid']) + " into outfile " + "'" + filepath + "'"+ """ FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\\n';"""
		print stmt
		engine.execute(stmt)
	print row['bid']
# DBSession = sessionmaker(bind=engine)
# DBSession.bind = engine
# session = DBSession()






# session.close()

    









