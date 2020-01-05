from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django import forms
from django.conf import settings
from .forms import MailSendForm, TemplateMailSendForm
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from .util.logger import logger
#import win32com.client
#import pythoncom
#import io
import urllib

import logging

log = logging.getLogger(__name__)

# Create your views here.
def index(request):
    log.info('index start')
    context = {
    }
    log.info('index end')
    return render(request, 'mytest/index.html', context)

def mail(request):
    log.info('mail start')
    log.info('mail method=[%s]' % request.method)
    
    mailsend_form = MailSendForm(request.POST or None)

    if request.method == 'POST' and mailsend_form.is_valid():
        send_mail( 
            mailsend_form.cleaned_data['subject'],
            mailsend_form.cleaned_data['mesage'],
            settings.DEFAULT_FROM_EMAIL,
            [mailsend_form.cleaned_data['to_mail']]
        )
        log.info('mail send success')
        log.info('mail end')
        return HttpResponseRedirect(reverse('mytest:index'))

    #mailsend_form.from_mail = settings.DEFAULT_FROM_EMAIL
    context = {
        'form':mailsend_form
    }
    log.info('mail end')
    return render(request, 'mytest/mail.html', context)


def templatemail(request):
    log.info('templatemail start')
    mailsend_form = TemplateMailSendForm(request.POST or None)
    
    if request.method == 'POST' and mailsend_form.is_valid():
        log.info( 'template=[' + mailsend_form.cleaned_data['mail_choices'] + ']')
        
        context = {
            'title':'メッセージタイトル',
            'user_name':'山田　太郎',
            'message':'めっせーじっ'
        }
        subject = 'Subject件名'
        #message = render_to_string('mytest/mail/01_template.txt', context, request )
        mail_template_file = ''
        if '1' == mailsend_form.cleaned_data['mail_choices'] :
            mail_template_file = 'mytest/mail/01_template.txt'
        elif '2' == mailsend_form.cleaned_data['mail_choices'] :
            mail_template_file = 'mytest/mail/02_template.txt'
        elif '3' == mailsend_form.cleaned_data['mail_choices'] :
            mail_template_file = 'mytest/mail/03_template.txt'
        message = render_to_string(mail_template_file, context )
        from_email = settings.DEFAULT_FROM_EMAIL  # 送信者
        recipient_list = ["test@test.co.jp"]  # 宛先リスト
        
        # メール送信実行
        send_mail(subject, message, from_email, recipient_list)
        log.info('mail send success')
        log.info('mail end')
        # indexへリダイレクト
        return HttpResponseRedirect(reverse('mytest:index'))

    context = {
        'form' : mailsend_form,
    }
    log.info('templatemail end')
    return render(request, 'mytest/templatemail.html', context)

#
# Excel ファイルのダウンロード
def download_excel(request):
    log.info('download_excel start')
    cnt = 0
    cnt = cnt + 1
    log.info('download_excel point %d' % cnt )

    try:
    
        # ファイルをバイナリモードでオープンし読込
        cnt = cnt + 1
        log.info('download_excel FileRead point %d' % cnt )
        buffer = open('C:/PycharmProjects4/strage/00.Python勉強.xlsx', mode='rb').read()
        log.info('download_excel HttpResponse作成 point %d' % cnt )
        cnt = cnt + 1
        # レスポンスオブジェクト生成
        response = HttpResponse(buffer, content_type='application/vnd.ms-excel')  # エクセルファイルを表す
        cnt = cnt + 1
        # ダウンロードファイル名設定
        log.info('download_excel ファイル名設定 point %d' % cnt )
        response['Content-Disposition'] = 'attachment; filename="{fn}"'.format(fn=urllib.parse.quote("00.Python勉強.xlsx"))
        cnt = cnt + 1
        log.info('download_excel Return point %d' % cnt )
    except Exception as e:
        print(dir(e))
        log.info(e)
        log.info('失敗')
        raise
    else:
        # 正常の場合レスポンスオブジェクトを返す
        log.info('成功')
        return response
    finally:
        log.info('download_excel end')

