# coding=utf-8
from __future__ import absolute_import
from ftplib import FTP
from ftplib import ftpcp
import os
import sys
import string
import datetime
import time
import socket
# import cherry.util.MyConfig
from cherry.util.config import conf_dict


class FtpClient:

    def __init__(self, hostaddr, username, password, remotedir, port=21):
        self.hostaddr = hostaddr
        self.username = username
        self.password = password
        self.remotedir = remotedir
        self.port = port
        self.ftp = FTP()
        self.file_list = []
        # self.ftp.set_debuglevel(2)

    def __del__(self):
        self.ftp.close()
        # self.ftp.set_debuglevel(0)

    def login(self):
        ftp = self.ftp
        try:
            timeout = 300
            socket.setdefaulttimeout(timeout)
            ftp.set_pasv(True)
            # print u'Connecting %s' %(self.hostaddr)
            ftp.connect(self.hostaddr, self.port)
            # print u'%s Connected' %(self.hostaddr)
            # print u'Begin to login %s' %(self.hostaddr)
            ftp.login(self.username, self.password)
            # print u'Login %s succeed' %(self.hostaddr)
#             debug_print(ftp.getwelcome())
        except Exception:
            print u'Login failed'
        try:
            ftp.cwd(self.remotedir)
        except(Exception):
            print u'Change dir failed'

    def download_file(self, localfile, remotefile):
        file_handler = open(localfile, 'wb')
        self.ftp.retrbinary(u'RETR %s' % (remotefile), file_handler.write)
        file_handler.close()

    def upload_file(self, localfile, remotefile):
        if not os.path.isfile(localfile):
            return
        file_handler = open(localfile, 'rb')

        remotedir = remotefile.split('/')
        for now_dir in remotedir[:-1]:
            try:
                self.ftp.mkd(now_dir)
            except:
                pass
            self.ftp.cwd(now_dir)
        self.ftp.storbinary('STOR %s' % remotedir[-1], file_handler)
        file_handler.close()
#         debug_print(u'Have delivered %s' % localfile)

    def delete_file(self, remotefile):
        return self.ftp.delete(remotefile)

    def list_file(self,file_path):
        self.ftp.cwd(file_path)
        return self.ftp.nlst()
    
    def get_file_list(self, line):
        ret_arr = []
        file_arr = self.get_filename(line)
        if file_arr[1] not in ['.', '..']:
            self.file_list.append(file_arr)

    def get_filename(self, line):
        pos = line.rfind(':')
        while(line[pos] != ' '):
            pos += 1
        while(line[pos] == ' '):
            pos += 1
        file_arr = [line[0], line[pos:]]
        return file_arr


hostaddr = conf_dict['ftp']['hostaddr']
username = conf_dict['ftp']['username']
password = conf_dict['ftp']['password']
port = conf_dict['ftp']['port']
rootdir_local = conf_dict['ftp']['rootdir_local']
rootdir_remote = conf_dict['ftp']['rootdir_remote']

f = FtpClient(hostaddr, username, password, rootdir_remote, port)


def upload_file(localfile, remotefile):
    f.login()
    f.upload_file(''.join([rootdir_local, localfile]),
                  ''.join([rootdir_remote, remotefile]))


def get_file(localfile, remotefile):
    f.login()
    f.download_file(
        ''.join([rootdir_local, localfile]),
        ''.join([rootdir_remote, remotefile]))
