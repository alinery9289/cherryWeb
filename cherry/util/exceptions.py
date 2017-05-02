# -*- coding: utf-8 -*-
from __future__ import absolute_import

from requests import RequestException as NetworkException


class DownloadError(NetworkException):
    '''Error when download'''


class UploadError(NetworkException):
    '''Error when upload'''


class FFmpegExecuteError(Exception):
    '''ffmpeg execute error'''


class GPACExecuteError(Exception):
    '''ffmpeg execute error'''


class InternalError(Exception):
    '''Internal error'''

class ParamterError(Exception):
    '''Paramter error'''
    
class MySQLError(Exception):
    '''Sql execute error'''