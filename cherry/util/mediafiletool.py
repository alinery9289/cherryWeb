from __future__ import absolute_import

import os
import subprocess

from datetime import datetime

from cherry.util.config import conf_dict
from cherry.util.sqltool import update_file_id_by_taskid, MediaFile, add_record



def add_new_file(download_cxt):
    output_file = download_cxt['output_file_path']
    (filepath,tempfilename) = os.path.split(output_file);
    (after_file_id,extension) = os.path.splitext(tempfilename);
    task_id = download_cxt['father_id']
    update_file_id_by_taskid(task_id,after_file_id)
    authcode = download_cxt['authcode']
    if os.path.isfile(output_file):
        encodeInfo = getEncodeInfo(output_file)[:800]
        filesize= os.path.getsize(output_file)
        new_file = MediaFile(fileid=after_file_id,filename=download_cxt['output_file_name'],authcode=authcode,filesize=filesize,location= output_file,filetype=extension,uploadtime= datetime.now(),encodeinfo= encodeInfo)
        add_record(new_file)

def getEncodeInfo(filename):
    getFileinfoCmd= "%s -show_format -i %s" % (conf_dict['tools']['ffprobe'],filename)

    process1 = subprocess.Popen(getFileinfoCmd, shell=True, stdout = subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines= True)
    encodeInfo=""
    while True:
        line = process1.stdout.readline()
        if not line:
            break
        lo = line.find('Duration:')
        if lo!=-1:
            encodeInfo+=line
        lo = line.find('Stream #0:')
        if lo!=-1:
            encodeInfo+=line

    return encodeInfo