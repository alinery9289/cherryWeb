
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cherry.util.config import conf_dict
from sqlalchemy.sql.sqltypes import BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, INTEGER, CHAR, DATETIME

from cherry.util.exceptions import MySQLError

db_username = conf_dict['mysql']['username']
db_password = conf_dict['mysql']['password']
db_host = conf_dict['mysql']['ip']
db_db_name = conf_dict['mysql']['db']

engine_info = "mysql+mysqldb://" + db_username + ":" + db_password + "@" + \
    db_host + "/" + db_db_name
engine = create_engine(engine_info)

Base = declarative_base()


class User(Base):
    __tablename__ = 'cherrymanage_user'
    authcode = Column(CHAR, primary_key=True, unique=True)
    email = Column(CHAR)
    userid = Column(CHAR)
    password = Column(CHAR)
    userstorage = Column(BigInteger)
    secretkey = Column(CHAR)
    outdate = Column(DATETIME)


class MediaFile(Base):
    __tablename__ = 'cherrymanage_mediafile'
    fileid = Column(CHAR, primary_key=True, unique=True)
    filename = Column(CHAR)
    authcode = Column(CHAR)
    filesize = Column(BigInteger)
    location = Column(CHAR)
    filetype = Column(CHAR)
    md5 = Column(CHAR)
    uploadtime = Column(DATETIME)
    encodeinfo = Column(CHAR)


class ProcessLog(Base):
    __tablename__ = 'cherrymanage_processlog'
    jobid = Column(CHAR, primary_key=True, unique=True)
    fileid = Column(CHAR)
    controljson = Column(CHAR)
    dealstate = Column(CHAR)
    dealtime = Column(DATETIME)
    completetime = Column(DATETIME)


class Task(Base):
    __tablename__ = 'cherrymanage_task'
    taskid = Column(CHAR, primary_key=True, unique=True)
    fatherid = Column(CHAR)
    afterfileid = Column(CHAR)
    dealmethod = Column(CHAR)
    dealstate = Column(CHAR)
    dealtime = Column(DATETIME)
    completetime = Column(DATETIME)

#sql create record
def add_record( new_record):
    try:
        Session = sessionmaker(bind=create_engine(engine_info))
        session = Session()
        session.add(new_record)
        session.commit()
        session.close()
    except Exception,e:
        raise MySQLError('could not add the task.%s :%s'%(Exception,e))
    
def update_dealstate_time_by_taskid(updated_taskid,updated_state):
    try:
        Session = sessionmaker(bind=create_engine(engine_info))
        session = Session() 
        updated_col = session.query(Task).filter( Task.taskid == updated_taskid)
        updated_col.update({Task.dealstate : updated_state,Task.completetime : datetime.now() })
        session.commit()
        session.close()
    except Exception,e:
        raise MySQLError('could not add the task.%s :%s'%(Exception,e))
    
def update_file_id_by_taskid(updated_taskid,file_id):
    try:
        Session = sessionmaker(bind=create_engine(engine_info))
        session = Session() 
        updated_col = session.query(Task).filter( Task.taskid == updated_taskid)
        updated_col.update({Task.afterfileid : file_id })
        session.commit()
        session.close()
    except Exception,e:
        raise MySQLError('could not add the task.%s :%s'%(Exception,e))
    
def update_processlog_by_job_id(job_id,deal_state):
    try:
        Session = sessionmaker(bind=create_engine(engine_info))
        session = Session() 
        updated_col = session.query(ProcessLog).filter( ProcessLog.jobid == job_id)
        updated_col.update({ProcessLog.dealstate : deal_state })
        session.commit()
        session.close()
    except Exception,e:
        raise MySQLError('could not add the task.%s :%s'%(Exception,e))
