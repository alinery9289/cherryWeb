# -*- coding: utf-8 -*-
'''
make task
author: huodahaha
date:2015/11/12
email:huodahaha@gmail.com
'''
from __future__ import absolute_import

import sys
from cherry.tasks.filters import filters_dict

from cherry.tasks.operators import (
    slicer, downloader, uploader, Merger, loader, backer, deleter)

from cherry.celery import celery_app

# upload,slice,download,merge直接由job_traker调用
# celery的异步任务只有filter类

def task_load(params):
    return loader.load(params)

def task_back(params):
    return backer.back(params)

def task_delete_cache(params):
    return deleter.delete_cache(params)

def task_upload(params):
    return uploader.upload(params)


def task_download(params):
    return downloader.download(params)


def task_slice(params):
    return slicer.slice(params)


def task_merge(params):
    merger = Merger()
    return merger.merge(params)


def generate_filter_task():
    task_dict = {}
    global filters_dict

#     for filter_name in filters_dict:
#         @celery_app.task(name='cherry.task.' + filter_name)
#         def filter_task(filter_params):
#             print("@filter_task: params %s" % filter_params)
#             _filter = filters_dict[filter_name]()
#             return _filter.do_process_main(filter_params)
#         task_dict[filter_name] = filter_task
#
#     return task_dict

    FUNC_TEMPLATE = "@celery_app.task(name='cherry.task.{func}')\ndef {func}(to_filter_para_in_str):\n\tprint sys._getframe().f_code.co_name\n\t"+\
            "anonymity_filter_instance = filters_dict['{func}']()\n\treturn anonymity_filter_instance.do_process_main(to_filter_para_in_str)"

    for fn in filters_dict:
        exec(FUNC_TEMPLATE.format(func=fn))

    local_vars = dict(locals().items())

    for fn in filters_dict:
        task_dict[fn] = local_vars[fn]

    return task_dict

task_dict = generate_filter_task()


# 以下为迭代算法

# group_num = check_from_DB(filters_dict)


# @celery_app.task(name='Cherry.Task.iteration_'+str(group_num))
# def filter_task(to_filter_para_in_str, filters):
#     for filter_i in filters:
#         to_filter_para_in_str = task_dict(filter_i)(to_filter_para_in_str)
#     return to_filter_para_in_str


# def check_from_DB(filters_dict):
#     '''
#     根据filters_dict 查找数据库，是否存在group，如果存在返回group_num,如果不存在，insert，生成一个新的group_num并返回
#     '''
#     pass

#     return group_num


task_dict['task_slice'] = task_slice
task_dict['task_merge'] = task_merge
task_dict['task_upload'] = task_upload
task_dict['task_download'] = task_download
task_dict['task_load'] = task_load
task_dict['task_back'] = task_back
task_dict['task_delete_cache'] = task_delete_cache