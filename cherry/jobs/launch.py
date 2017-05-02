# -*- coding: utf-8 -*-
"""
launch.py

Launch jobs, locally, or remotely.

author: huodahaha, zhangxusheng,
        Yanan Zhao <arthurchiao@hotmail.com>
date:2016/10/21
last modified: 2016-11-01 17:38:59
"""
from __future__ import absolute_import

import time
import copy
# from celery.result import AsyncResult


from cherry.celery import celery_app
from cherry.tasks.tasks import task_dict
from cherry.util.mediafiletool import add_new_file
from cherry.util.sqltool import update_processlog_by_job_id
    
@celery_app.task(name='cherry.task.sliced_job')
def launch_sliced_job(context):
    """job: in json format
    """
    
    filters = context['filters']
    slicer_cxts = task_dict['task_slice'](context)
    slicer_nums = len(slicer_cxts)
    subtasks_id = []
    
    try:
        for slicer_cxt in slicer_cxts:
            res = task_dict['task_upload'](slicer_cxt)
            for i,one_filter in enumerate(filters):   
                one_res = copy.deepcopy(res)
                one_res['filters'] = {}
                one_res['filters'] = one_filter
                one_res['index_series'] = i
                task = task_dict[one_filter.keys()[0]].delay(one_res)
                subtasks_id.append(task.id)
        index_list_dict = {}      
        while subtasks_id:
    #         del_list = []
            for one_id in subtasks_id:
                subtasks_id_result = celery_app.AsyncResult(one_id);
                if subtasks_id_result.successful():
                    # print "OK!"
    #                 del_list.append(i)
                    cxt_list = subtasks_id_result.get()
                    for one_cxt_json in cxt_list:
                        if (not one_cxt_json.has_key('filters') or one_cxt_json['filters']=={}):
                            download_cxt = task_dict['task_download'](one_cxt_json)#知道已经结束，开始最后的下载，但是未记录
                            index_list = download_cxt['index_list']
                            if index_list_dict.has_key(index_list):
                                if (index_list_dict[index_list]>=slicer_nums-1):
                                    download_cxt['slicer_nums'] = slicer_nums
                                    task_dict['task_merge'](download_cxt)
                                    add_new_file(download_cxt)#添加数据库
                                    index_list_dict.pop(index_list)
                                else:
                                    index_list_dict[index_list] +=1
                            else :
                                index_list_dict[index_list] =1
                            
                            #判断是否需要合成，将现有文件对应的列表值加1，然后判断是否达到规定值
                        else:
                            next_filter = one_cxt_json['filters'].keys()[0]
                            time.sleep(0.1)
                            next_task = task_dict[next_filter].delay(one_cxt_json)
    #                         next_task = task_dict[next_filter](one_cxt_json)
                            subtasks_id.append(next_task.id)
                    subtasks_id.remove(one_id)
                elif subtasks_id_result.failed():
                    print "error"
                    subtasks_id.remove(one_id)    
            time.sleep(1)
        update_processlog_by_job_id(res['job_id'],'succeed')
    except Exception,e:
        raise IOError("error: %s" % str(e))
    finally:
        task_dict['task_delete_cache'](res)
 
@celery_app.task(name='cherry.task.intact_job')
def launch_intact_job(context):
    """job: in json format
    """
    
    filters = context['filters']
    load_ret = task_dict['task_load'](context)
    
    subtasks_id = []
    try:
        
        res = task_dict['task_upload'](load_ret)
        for i,one_filter in enumerate(filters):   
            one_res = copy.deepcopy(res)
            one_res['filters'] = {}
            one_res['filters'] = one_filter
            one_res['index_series'] = i
            task = task_dict[one_filter.keys()[0]].delay(one_res)
            subtasks_id.append(task.id)
              
        while subtasks_id:
    #         del_list = []
            for one_id in subtasks_id:
                subtasks_id_result = celery_app.AsyncResult(one_id);
                if subtasks_id_result.successful():
                    # print "OK!"
    #                 del_list.append(i)
                    cxt_list = subtasks_id_result.get()
                    for one_cxt_json in cxt_list:
                        if (not one_cxt_json.has_key('filters') or one_cxt_json['filters']=={}):
                            download_cxt = task_dict['task_download'](one_cxt_json)#知道已经结束，开始最后的下载，但是未记录
                            task_dict['task_back'](download_cxt)
                            add_new_file(download_cxt)#添加数据库
                            #判断是否需要合成，将现有文件对应的列表值加1，然后判断是否达到规定值
                        else:
                            next_filter = one_cxt_json['filters'].keys()[0]
                            time.sleep(0.1)
                            next_task = task_dict[next_filter].delay(one_cxt_json)
    #                         next_task = task_dict[next_filter](one_cxt_json)
                            subtasks_id.append(next_task.id)
                    subtasks_id.remove(one_id)
                elif subtasks_id_result.failed():
                    print "error"
                    subtasks_id.remove(one_id)    
            time.sleep(1)
        update_processlog_by_job_id(res['job_id'],'succeed')
    except Exception,e:
        raise IOError("error: %s" % str(e))
    finally:
        task_dict['task_delete_cache'](load_ret)
        

    
