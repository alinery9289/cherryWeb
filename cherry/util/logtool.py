from __future__ import absolute_import

import os
import time 

import logging.handlers
from cherry.util.config import conf_dict

log_path = conf_dict['all']['log_path']  
  
fmt = '%(asctime)s [%(levelname)s] %(message)s' 
datefmt='%a, %d %b %Y %H:%M:%S' 
formatter = logging.Formatter(fmt= fmt)

class Singleton(object):
    """Singleton decorator
    """
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

class Logger(Singleton):
    
    def __init__(self):
        super(Logger, self).__init__()
        timeArray = time.localtime()
        otherStyleTime = time.strftime("%Y_%m_%d", timeArray)
        self.this_log = logging.getLogger(otherStyleTime+'_main_log')
        self.this_handler= logging.handlers.RotatingFileHandler(filename= os.path.join(log_path,otherStyleTime+'_main_log.log'), maxBytes= 10*1024*1024)  
        self.this_handler.setFormatter(formatter)
        self.this_log.addHandler(self.this_handler)
        self.this_log.setLevel(logging.DEBUG) 
        
    def debug(self, msg):
        self.this_log.debug(msg)
        
    def info(self, msg):
        self.this_log.info(msg)
        
    def warning(self, msg):
        self.this_log.warning(msg)
        
    def error(self, msg):
        self.this_log.error(msg)
        
    def release(self):
        self.this_log.removeHandler(self.this_handler)

class TaskLogger(Singleton):
    
    def __init__(self,taskid):
        super(TaskLogger, self).__init__()
        self.taskid = taskid
        self.this_log = logging.getLogger(taskid+'_log')
        if (os.path.exists(os.path.join(log_path,'transcode_log'))== False):    
            os.mkdir(os.path.join(log_path,'transcode_log'))
        self.this_handler= logging.handlers.RotatingFileHandler(os.path.join(log_path,'transcode_log',taskid+'_log.log'))
        self.this_handler.setFormatter(formatter)
        self.this_log.addHandler(self.this_handler)
        self.this_log.setLevel(logging.DEBUG) 
        
    def debug(self, msg):
        self.this_log.debug(msg)
        
    def info(self, msg):
        self.this_log.info(msg)
        
    def warning(self, msg):
        self.this_log.warning(msg)
        
    def error(self, msg):
        self.this_log.error(msg)
    
    def release(self):
        self.this_log.removeHandler(self.this_handler)