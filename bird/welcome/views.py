# Create your views here.
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from form import PhoneNoForm
from publicfun import log
import publicfun
from dboperation import db
from iptables import iptable


def GetClientIPAndUrl(request):
    for k, v in request.GET.items():
        log("GET[%s] = %s" % (k, v))
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    try:
        before_url = request.META.get('HTTP_HOST')
    except:
        before_url = ''
    return ip, before_url


def welcome(request):
    ip, before_url = GetClientIPAndUrl(request)
    log('ip = %s, url = %s' % (ip, before_url))
    if request.method == 'POST':
        form = PhoneNoForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            phoneno = form_data['phone_no']
            verifyno = form_data['verify_no']            
            for k, v in request.POST.items():
                log("POST[%s] = %s" % (k, v))
            if request.POST.has_key('phone'):
                if not publicfun.CheckPhoneNo(phoneno):
                    phone_no_error = True
                    error_message = "您输入的手机号码有误，请重新输入！"
                    tmp_phone_no = phoneno
                    return render_to_response('welcomebase.html', locals())
                else:
                    # check phone_no in db
                    wait_verify_db = db()
                    if wait_verify_db.check_phone_online(phoneno):
                        log('phone is exsit')
                        phone_no_error = True
                        error_message = "您的手机号已经使用过，请换一个手机号验证！"
                        return render_to_response('welcomebase.html', locals())
                    else:  # save to database
                        wait_verify_db.SaveToTable_WaitForVerify(ip, phoneno, publicfun.GenerateRandomNo())
                        tmp_phone_no = phoneno
                        return render_to_response('welcomebase.html', locals())
            elif request.POST.has_key('verify'):
                # read db check verifyno
                log('verifyno=%s' % verifyno)
                stDB = db()
                if not stDB.check_verify_no(verifyno, phoneno):
                    verify_no_error = True
                    error_message = "您输入的验证码有误，请重新输入！"
                    tmp_phone_no = phoneno
                    tmp_verify_no = verifyno
                    return render_to_response('welcomebase.html', locals())
                else:
                    # save to database
                    stDB.SaveToTable_OnLine(ip, phoneno)
                    stDB.SaveToTable_HistoryInfo(phoneno)
                    stDB.Delete_WaitForVerify_phone(phoneno)
                    #add to iptable
                    rule = iptable()
                    rule.add_nat_rule(ip)
                    # direct
                    if not before_url:
                        log('url is empty')
                        return HttpResponseRedirect("http://www.baidu.com")
                    else:
                        log('url = %s' % before_url)
                        if 'http' not in before_url:
                            before_url = 'http://' + before_url
                        return HttpResponseRedirect(before_url)
                    # return HttpResponseRedirect(request.META['REFEREN'])
                    
            else:
                return HttpResponse('bad error')
    else:
        return render_to_response('welcomebase.html')

    # if 'phoneno' in request.GET:
    #     phoneno = request.GET['phoneno']
    #     if not publicfun.CheckPhoneNo(phoneno):
    #         errormsg = "您输入的手机号码有误，请重新输入！"
    #         return render_to_response('welcome_error.html', {'ErrorMessage': errormsg})
    #     else:
    # check phone_no in db
    #         wait_verify_db = db()
    #         if wait_verify_db.check_phone_online(phoneno):
    #             errormsg = "您的手机号已经使用过，请换一个手机号验证！"
    #             return render_to_response('welcome_error.html', {'ErrorMessage': errormsg})
    # else:  # save to database
    #             wait_verify_db.SetTable_WaitForVerify(
    #                 GetClientIP(request), phoneno, publicfun.GenerateRandomNo())
    #         return render_to_response('welcome_no_error.html')

    # return render_to_response('welcome_no_error.html')


def verify_no(request):
    return HttpResponseRedirect("http://www.baidu.com")
    # if 'verifyno' in request.GET:
    # check verify_no in db
    #     wait_verify_db = db()
    #     if wait_verify_db.check_verify_no():
    #         pass

def hello(request):
    return HttpResponse('hello')
    # if request.method == 'POST':
    #     form = PhoneNoForm(request.POST)
    #     for k, v in request.POST.items():
    #         log("POST[%s] = %s" % (k, v))
    #     # form = PhoneNoForm({'phone_no': '123', 'verifyno': '2'})
    #     if form.is_valid():
    #         log("form.cleaned_data = %s" % form.cleaned_data['phone_no'])
    #         data = form.cleaned_data
    #         phone_no = data['phone_no']
    #         log('phone_no = %s' % phone_no)
    #         # return render_to_response('result.html', {'phone_no': phone_no})
    #         return HttpResponse('hello')
    # return render_to_response('result.html')
    # cd = form.cleaned_data
    # phone_no = cd['phone_no']
    # return render_to_response('result.html', {'phone_no': phone_no})

def hehe(request):
    for k, v in request.META.items():
        log("META[%s] = %s" % (k, v))
    return HttpResponse('hehe')