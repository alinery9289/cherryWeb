"""cherryWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'cherryManage.views.transcodePage', name='transcodePage'), 
    url(r'^transcode$', 'cherryManage.views.transcodePage', name='transcodePage'), 
    url(r'^filelist$', 'cherryManage.views.filelistPage', name='filelistPage'), 
#     user Proc
    url(r'^user$', 'cherryManage.views.userProc', name='userProc'),
    url(r'^user/authcode/([a-zA-Z0-9]{32})$', 'cherryManage.views.userAuthProc', name='userProc'),
    url(r'^user/Registration$', 'cherryManage.views.userRegistrationProc', name='userRegistrationProc'),
#     file Proc
    url(r'^mediafile$', 'cherryManage.views.mediaFileProc', name='mediaFileProc'),
    url(r'^mediafile/fileid/([a-zA-Z0-9]{32})/authcode/([a-zA-Z0-9]{32})$', 'cherryManage.views.mediaFileByIdProc', name='mediaFileByIdProc'),
    url(r'^mediafile/info/fileid/([a-zA-Z0-9]{32})$', 'cherryManage.views.mediaFileInfoByIdProc', name='mediaFileInfoByIdProc'),    
    url(r'^mediafile/info/authcode/([a-zA-Z0-9]{32})$', 'cherryManage.views.mediaFileInfoByAuthProc', name='mediaFileInfoByAuthProc'),
    
    url(r'^ftpmediafilename/authcode/([a-zA-Z0-9]{32})$', 'cherryManage.views.ftpMediaFileName', name='ftpMediaFileName'),
    url(r'^ftpmediafile$', 'cherryManage.views.ftpMediaFileProc', name='ftpMediaFileProc'),
    url(r'^ftpmediafile/fileid/([a-zA-Z0-9]{32})/authcode/([a-zA-Z0-9]{32})$', 'cherryManage.views.ftpMediaFileByIdProc', name='ftpMediaFileByIdProc'),
    
    url(r'^h264tohevc$', 'cherryManage.views.H264toHevcProc', name='H264toHevcProc'), 
    url(r'^h264tohevc/allinfo/authcode/([a-zA-Z0-9]{32})$', 'cherryManage.views.H264toHevcInfoByAuthProc', name='H264toHevcInfoByAuthProc'),
    url(r'^h264tohevc/info/jobid/([a-zA-Z0-9]{32})$', 'cherryManage.views.H264toHevcInfoProc', name='H264toHevcInfoProc'),
]
