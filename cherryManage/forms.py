#-*- coding:utf-8 -*-
'''
Created on 2015.7.21

@author: Zhangxusheng
'''

from django import forms
 
class AddUserForm(forms.Form):
    userid = forms.CharField()
    password = forms.CharField()
    check_password = forms.CharField()
    email = forms.CharField()

class UserLoginForm(forms.Form):
    userid = forms.CharField()
    password = forms.CharField()

class UploadForm(forms.Form):
    fileList = forms.FileField()
    
class AuthUploadForm(forms.Form):
    authcode = forms.CharField()
    fileList = forms.FileField()

class ftpFileForm(forms.Form):
#     authcode = forms.CharField()
#     filename = forms.CharField()
    jobs = forms.CharField()