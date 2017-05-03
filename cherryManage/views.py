#-*- coding:utf-8 -*- 
# from __future__ import absolute_import

import os
import json
import uuid
import Queue

from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse,StreamingHttpResponse
from forms import UserLoginForm,AddUserForm,AuthUploadForm,ftpFileForm
from models import user,mediafile, processlog,task 
from methods import md5,filesizeChange,usernameExist,emailExist,handleAllUploadedFile,\
updateAuthStorage,handleFtpFile,copyfiletoUser,check_filters,update_out_file_path,file_iterator
from datetime import datetime
from cherry.util.config import conf_dict
from cherry.util.redistool import redis_get,redis_set, redis_has_key, redis_del
from cherry.jobs.launch import *
from django.template.context_processors import request

httpstr = conf_dict['all']['httpstr']
userftp = conf_dict['all']['userftp']
storageftp = conf_dict['all']['storageftp']

def transcodePage(request):
    return render(request, 'transcode.html')

def filelistPage(request):
    return render(request, 'filelist.html')

def userProc(request):
    if request.method == 'POST':# 当提交表单时
     
        form = UserLoginForm(request.POST) # form 包含提交的数据
         
        if form.is_valid():# 如果提交的数据合法
            username =str( form.cleaned_data['userid'])
            password = str( form.cleaned_data['password'])
            #print authcode1+" "+username1+" "+password1+" "+email1
            this_users = user.objects.filter(userid = username)
            if this_users.count() > 0 :
                for this_user in list(this_users):
                    if this_user.password == md5(password):
                        response =HttpResponseRedirect(request.META['HTTP_REFERER'])
                        
                        response.set_cookie("authcode",this_user.authcode, 24*60*60)
                        return response
                    else : return HttpResponse('Error: The password is wrong! <a href="/">Click to login again!</a>')
                    break
            else : return HttpResponse('Error: Don\'t have this user ! <a href="/">Click to register first!</a>')
        else: return HttpResponse('Error: Can\'t login! <a href="/">Click to login again.</a>')

def userAuthProc(request,authcode):
    if request.method == 'GET':# 当提交表单时
        
        this_users = user.objects.filter(authcode = authcode)
        
        if this_users.count() > 0 :
            for this_user in list(this_users):
                response_data = {}
                response_data['username'] = this_user.userid
                response_data['storage'] = filesizeChange(this_user.userstorage)
                return HttpResponse(json.dumps(response_data), content_type="application/json")
        else : return HttpResponse('Error: Something wrong! <a href="/">Click to login again!</a>')

def userRegistrationProc(request):
    if request.method == 'POST':# 当提交表单时
     
        form = AddUserForm(request.POST) # form 包含提交的数据
         
        if form.is_valid():# 如果提交的数据合法
            authcode1=str(uuid.uuid1()).replace('-','')
            username1 =str( form.cleaned_data['userid'])
            password1 = str( form.cleaned_data['password'])
            password2 = str( form.cleaned_data['check_password'])
            email1 = str( form.cleaned_data['email'])
            #print authcode1+" "+username1+" "+password1+" "+email1
            if usernameExist(username1) > 0 :
                return HttpResponse('The username already exist! <a href="/">Click to register again.</a>')
            if emailExist(email1) > 0 :
                return HttpResponse('The email already exist! <a href="/">Click to register again.</a>')
            
            if password1==password2:
                oneUser = user(authcode=authcode1,userid=username1,password=md5(password1),email=email1,userstorage=0)
                oneUser.save()
                return HttpResponse('Register ok! <a href="/">Click to back.</a>')
            else : return HttpResponse('Error: The two password are different! <a href="/">Click to register again.</a>')
        else: return HttpResponse('Error: Can\'t register! <a href="/">Click to register again.</a>')
        
def mediaFileProc(request):
    if request.method == 'POST':
        form = AuthUploadForm(request.POST, request.FILES)
        if form.is_valid():
            authcode =str( form.cleaned_data['authcode'])
            saveResult=handleAllUploadedFile(request.FILES.getlist("fileList"),authcode)
            updateAuthStorage(authcode)
            return HttpResponse(saveResult)
    return HttpResponse("Error")

def ftpMediaFileName(request,authcode):
    if request.method == 'GET':
        response_data ={}
        list1= []
        list2= os.listdir(userftp+'upload')
        for a in list2:
            b= a.decode('gbk')
            list1.append(b)
        response_data["fileList"]=list1
        return HttpResponse(json.dumps(response_data,ensure_ascii=False,encoding='utf-8'), content_type="application/json")
    return HttpResponse("Error")
    
def ftpMediaFileProc(request):
    if request.method == 'POST':
        form = ftpFileForm(request.POST)
        if form.is_valid():
            authcode =str( form.cleaned_data['authcode'])
            filename =str( form.cleaned_data['filename'])
            saveResult=handleFtpFile(authcode,filename)
            updateAuthStorage(authcode)
            return HttpResponse(saveResult)
    return HttpResponse("Error")

def ftpMediaFileByIdProc(request, fileid, authcode):
    if  request.method == 'GET':
        onefile = mediafile.objects.get(fileid = fileid)
        if onefile.authcode==authcode:
            try:
                copyfiletoUser(onefile.location,onefile.filename)
                return HttpResponse("succeed")
            except EOFError:
                return HttpResponse("error")  
    return HttpResponse("error")  

def H264toHevcProc(request):
    if request.method == 'POST':
        form = ftpFileForm(request.POST)
        if form.is_valid():
            filterparam = str( form.cleaned_data['jobs'])
            filterparam_json = json.loads(filterparam)
            authcode = filterparam_json['authcode']
            input_file_name = filterparam_json.pop('input_file_name')
            filterparam_json['is_local']=(int)(filterparam_json['is_local'])
            #add to file manage system
            if (len(user.objects.filter(authcode = authcode))==0):
                return HttpResponse("Error: No authorized user.")
            if (not check_filters(filterparam_json['filters'])):
                return HttpResponse("Error: filters error.")  
            fileid=handleFtpFile(authcode,input_file_name)            
            if (fileid=="error"):
                return HttpResponse("Error: Get file failed.")
            #update user table
            updateAuthStorage(authcode)
            #add process(task) log  
            
            job_id= str(uuid.uuid1()).replace('-','')
#             for oneProcess in filterparam_json['filters']:  
            filterparam_json['input_file_path'] = ''.join([ storageftp, '.'.join([fileid, input_file_name.split('.')[-1]])])
            filterparam_json['job_id'] = job_id
            for one_filter in filterparam_json['filters']:
                update_out_file_path(one_filter)
            
            oneProcesslog = processlog(jobid=job_id, fileid=fileid,controljson=filterparam_json, 
                                       dealstate="processing",dealtime= datetime.now())
            oneProcesslog.save()      
            slice_type = filterparam_json.pop("slice_type")
            
            redis_set('_'.join(["task","status",job_id]),"Pending the job...")
            if (slice_type=="intact"):   
                launch_intact_job.delay(filterparam_json)
            elif(slice_type=="sliced"):
                launch_sliced_job.delay(filterparam_json)
            return HttpResponse(job_id)
    return HttpResponse("Error")

def H264toHevcInfoProc(request,jobid):
    if request.method == 'GET':
        job_logs = processlog.objects.filter(jobid = jobid)
        queue = Queue.Queue()
        queue.put(jobid)
        for job_log in job_logs:
            if job_log.dealstate=="succeed":
                redis_del('_'.join(["task","status",jobid]))
                while ( not queue.empty()):
                    father_id = queue.get()
                    next_ids = task.objects.filter(fatherid = father_id)
                    for next_id in next_ids:
                        redis_del('_'.join(["task","status",next_id.taskid]))
                return HttpResponse("All complete!")
        processingTask = []
        processingTask.append(redis_get('_'.join(["task","status",jobid])))
        while ( not queue.empty()):
            father_id = queue.get()
            next_ids = task.objects.filter(fatherid = father_id)
            for next_id in next_ids:
                queue.put(next_id.taskid)
                if (redis_has_key('_'.join(["task","status",next_id.taskid]))):
                    processingTask.append(redis_get('_'.join(["task","status",next_id.taskid])))
        if len(processingTask)==0:
            return HttpResponse("Error")
        else :
            return HttpResponse("\n".join(processingTask))
    return HttpResponse("Error")

def H264toHevcInfoByAuthProc(request,authcode):
    if request.method == 'GET':
        dealfiles = mediafile.objects.filter(authcode = authcode)
        response_datas = []
        if dealfiles.count() >0:
            one_dict={}
            fileids = []
            for dealfile in list(dealfiles):
                fileids.append(dealfile.fileid)
                one_dict[dealfile.fileid] = dealfile.filename
            processlogs = processlog.objects.filter(fileid__in = fileids, dealstate__in = ['raw','pending','processing']).order_by('-dealtime')
            if processlogs.count()>0:
                for oneprocesslog in list(processlogs):
                    response_data ={}
                    response_data["jobid"]=oneprocesslog.jobid
                    response_data["fileid"]=oneprocesslog.fileid
                    response_data["filename"]=one_dict[oneprocesslog.fileid]
                    response_datas.append(response_data)
            return HttpResponse(json.dumps(response_datas), content_type="application/json")
        return HttpResponse(json.dumps(response_datas), content_type="application/json")
    return HttpResponse('error')
    
def mediaFileByIdProc(request, fileid, authcode):
    if request.method == 'GET':
        this_files = mediafile.objects.filter(fileid = fileid)
        if this_files.count() > 0 :
            for this_file in list(this_files):
                if (authcode != this_file.authcode):
                    return HttpResponse("the file and the user don't match!")
                response = StreamingHttpResponse(file_iterator(this_file.location))
                response['Content-Type'] = 'application/octet-stream;charset=UTF-8'
                response['Content-Disposition'] = 'attachment; filename=%s' % this_file.filename
            return response
        else: return HttpResponse("Don't have this file!")
    elif request.method == 'DELETE':
        this_files = mediafile.objects.filter(fileid = fileid)
        filename = ""
        if this_files.count() > 0 :
            for this_file in list(this_files):
                if (authcode != this_file.authcode):
                    return HttpResponse("the file and the user don't match!")
                filename= this_file.filename
                this_file.delete()
                if os.path.exists(this_file.location):
                    os.remove(this_file.location)
            updateAuthStorage(authcode)
        this_logs = processlog.objects.filter(fileid = fileid)
        if this_logs.count()>0 :
            for this_log in list(this_logs):
                queue = Queue.Queue()
                queue.put(this_log.jobid)
                while ( not queue.empty()):
                    father_id = queue.get()
                    next_ids = task.objects.filter(fatherid = father_id)
                    for next_id in next_ids:
                        next_id.delete()
                this_log.delete()
        return HttpResponse('File '+ filename +' delete ok!')

def mediaFileInfoByIdProc(request, fileid, authcode):
    if request.method == 'GET':
        this_files = mediafile.objects.filter(fileid = fileid)
        if this_files.count() > 0 :
            for this_file in list(this_files):
                if (authcode != this_file.authcode):
                    return HttpResponse("the file and the user don't match!")
                response_data ={}
                response_data["fileid"]=fileid
                response_data["filename"]=this_file.filename
                response_data["authcode"]=this_file.authcode
                response_data["location"]=''.join([httpstr,this_file.fileid,'/authcode/',this_file.authcode])
                response_data["filesize"]=filesizeChange(this_file.filesize)
                response_data["filetype"]=this_file.filetype
                response_data["uploadtime"]=this_file.uploadtime.strftime("%Y-%m-%d %H:%M:%S")
                response_data["encodeinfo"]=this_file.encodeinfo
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        
def mediaFileInfoByAuthProc(request,authcode):
    if request.method == 'GET':
        this_files = mediafile.objects.filter(authcode = authcode).order_by("-uploadtime")
        response_datas = []
        if this_files.count() > 0 :
            for this_file in list(this_files):
                response_data ={}
                response_data["fileid"]=this_file.fileid
                response_data["filename"]=this_file.filename
                response_data["location"]=''.join([httpstr,this_file.fileid,'/authcode/',this_file.authcode])
                response_data["filesize"]=filesizeChange(this_file.filesize)
                response_data["filetype"]=this_file.filetype
                response_data["uploadtime"]=this_file.uploadtime.strftime("%Y-%m-%d %H:%M:%S")
                response_data["encodeinfo"]=this_file.encodeinfo
                response_datas.append(response_data)
            return HttpResponse(json.dumps(response_datas), content_type="application/json")
        else : return HttpResponse(json.dumps(response_datas), content_type="application/json")
        
def StateProc(request):
    if request.method == 'GET':
        response_data = {}
        processed_processlogs = processlog.objects.filter(dealstate='processing')
        response_data['processing_jobs']= processed_processlogs.count()
        succeed_processlogs = processlog.objects.filter(dealstate='succeed')
        response_data['succeed_jobs']= succeed_processlogs.count()
        failed_processlogs = processlog.objects.filter(dealstate='failed')
        response_data['failed_jobs']= failed_processlogs.count()
        processed_tasks = task.objects.filter(dealstate='processing')
        response_data['processing_tasks']= processed_tasks.count()
        succeed_tasks = task.objects.filter(dealstate='succeed')
        response_data['succeed_tasks']= succeed_tasks.count()
        failed_tasks = task.objects.filter(dealstate='failed')
        response_data['failed_tasks']= failed_tasks.count()
        return HttpResponse(json.dumps(response_data), content_type="application/json")