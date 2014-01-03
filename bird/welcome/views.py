# Create your views here.
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response
import logging
import models
import publicfun
import dboperation

def GetClientIP(request):
    logging.basicConfig(filename='example.log',level=logging.DEBUG,\
        format='%(asctime)s %(message)s')
    for k, v in request.COOKIES.items():
        logging.warning("COOKIES[%s] = %s" % (k ,v))
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def welcome(request):
    # if request.method == 'GET':
    #     errormsg = 'Get Method'
    #     return render_to_response('welcome.html', {'ErrorMessage': errormsg})
    # elif request.method == 'POST':
    #     errormsg = 'POST Method'
    #     return render_to_response('welcome.html', {'ErrorMessage': errormsg})
    
    if 'phoneno' in request.GET:
        phoneno = request.GET['phoneno']
        if not publicfun.CheckPhoneNo(phoneno):
            errormsg = "您输入的手机号码有误，请重新输入!"
            return render_to_response('welcome_error.html', {'ErrorMessage': errormsg})
        else:
            setdb = dboperation.db()
            setdb.SetTable_WaitForVerify(GetClientIP(request), phoneno, publicfun.GenerateRandomNo())
            return render_to_response('result.html', {'phoneno': phoneno})

    return render_to_response('welcome_no_error.html')




# def handleResult(request):
