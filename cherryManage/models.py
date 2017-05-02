
from django.db import models

# Create your models here.
class user(models.Model):
    authcode = models.CharField(max_length=32,primary_key=True,unique=True)
    email = models.CharField(max_length=45,unique=True)
    userid = models.CharField(max_length=16,unique=True)
    password = models.CharField(max_length=32)
    userstorage = models.BigIntegerField()
    secretkey = models.CharField(max_length=45,unique=True,blank=True,null=True)
    outdate = models.DateTimeField(blank=True,null=True)
    
class mediafile(models.Model):
    fileid = models.CharField(max_length=32,primary_key=True,unique=True)
    filename = models.CharField(max_length=100)
    authcode = models.CharField(max_length=32)
    filesize = models.BigIntegerField()
    location = models.CharField(max_length=200)
    filetype = models.CharField(max_length=10,blank=True,null=True)
    md5 = models.CharField(max_length=45,blank=True,null=True)
    uploadtime = models.DateTimeField()
    encodeinfo = models.CharField(max_length=1200,blank=True,null=True)
    
class processlog(models.Model):
    jobid = models.CharField(max_length=32,primary_key=True,unique=True)
    fileid = models.CharField(max_length=32)
    controljson =  models.CharField(max_length=1000)
    dealstate =  models.CharField(max_length=45)
#     afterfileid = models.CharField(max_length=32,blank=True,null=True)
    dealtime = models.DateTimeField()
    completetime = models.DateTimeField(blank=True,null=True)
    
class task(models.Model):
    taskid = models.CharField(max_length=32,primary_key=True,unique=True)
    fatherid = models.CharField(max_length=32,db_index=True)
    afterfileid = models.CharField(max_length=32,blank=True,null=True)
    dealmethod = models.CharField(max_length=45)
    dealstate = models.CharField(max_length=45)
    dealtime = models.DateTimeField()
    completetime = models.DateTimeField(blank=True,null=True)
    