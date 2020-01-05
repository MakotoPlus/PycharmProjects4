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
import win32com.client
import pythoncom
import io
import os
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
        buffer = open('C:/PycharmProjects4/strage/最新営業状況.xlsx', mode='rb').read()
        log.info('download_excel HttpResponse作成 point %d' % cnt )
        cnt = cnt + 1
        # レスポンスオブジェクト生成
        response = HttpResponse(buffer, content_type='application/vnd.ms-excel')  # エクセルファイルを表す
        cnt = cnt + 1
        # ダウンロードファイル名設定
        log.info('download_excel ファイル名設定 point %d' % cnt )
        response['Content-Disposition'] = 'attachment; filename="{fn}"'.format(fn=urllib.parse.quote("最新営業状況.xlsx"))
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

#
# PDF ファイルのダウンロード
def download_pdf(request):
    log.info('download_pdf start')
    cnt = 0
    cnt = cnt + 1
    log.info('download_pdf point %d' % cnt )
    try:
        # ファイルをバイナリモードでオープンし読込
        cnt = cnt + 1
        log.info('download_pdf FileRead point %d' % cnt )
        buffer = open('C:/PycharmProjects4/strage/Test_EDC.pdf', mode='rb').read()
        log.info('download_pdf HttpResponse作成 point %d' % cnt )
        cnt = cnt + 1
        # レスポンスオブジェクト生成
        response = HttpResponse(buffer, content_type='application/pdf')  # PDFファイルを表す
        cnt = cnt + 1
        # ダウンロードファイル名設定
        log.info('download_pdf ファイル名設定 point %d' % cnt )
        response['Content-Disposition'] = 'attachment; filename="{fn}"'.format(fn=urllib.parse.quote("Test_EDC.pdf"))
        cnt = cnt + 1
        log.info('download_pdf Return point %d' % cnt )
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
        log.info('download_pdf end')

#
# Excel For PDF ファイルのダウンロード
def download_excel_for_pdf(request):
    method_name ='download_excel_for_pdf '
    pythoncom.CoInitialize()  # Excelを起動する前にこれを呼び出す
    excel = win32com.client.Dispatch("Excel.Application")
    log.info(method_name + 'start')
    cnt = 0
    cnt = cnt + 1
    log.info('%s point %d' % ( method_name, cnt ))
    cnt = cnt + 1
    log.info('%s point %d' % ( method_name, cnt ))
    excel.Visible = False
    excel.DisplayAlerts = False
    cnt = cnt + 1
    log.info('%s point %d' % ( method_name, cnt ))

    #ExcelFileName = 'C:/PycharmProjects4/strage/最新営業状況.xlsx'
    ExcelFileName = 'C:/PycharmProjects4/strage/（A2機密）SAMPLE_ABC製薬株式会社様(ABC111の使用成績調査)_EDC.xlsx'
    
    try:
        wb = excel.Workbooks.Open(ExcelFileName)
        
        #不要のシートを削除
        #sheets = ('【速報】稼働人数','12月スクランブル', '訪問管理','BP800戦略_定例会日程','Sample_コミュニケーション',)
        sheets = ('使用方法','FZ原価（解析）', '平成30年料金表（解析）','入力シート','原価_MW','入力シート (2)','原価（安全性）','Sheet1',)
        cnt = cnt + 1
        log.info('%s Sheet Delete point %d' % ( method_name, cnt ))
        for sheet in sheets:
            log.info('%s Sheet [%s] Delete point %d' % ( method_name, sheet, cnt ))
            #wb.WorkSheets(sheet).Activate()
            log.info('%s Sheet [%s] Delete point %d' % ( method_name, sheet, cnt ))
            wb.WorkSheets(sheet).Delete()

        cnt = cnt + 1
        log.info('%s Sheet IsFileCheck PDF point %d' % ( method_name, cnt ))
        if os.path.isfile('C:/PycharmProjects4/strage/Test_EDC_2.pdf'):
            #ファイル削除
            log.info('%s Sheet PDF Remove point %d' % ( method_name, cnt ))
            os.remove('C:/PycharmProjects4/strage/Test_EDC_2.pdf')

        cnt = cnt + 1
        log.info('%s Sheet PDF Export point %d' % ( method_name, cnt ))
        wb.ExportAsFixedFormat(0, 'C:/PycharmProjects4/strage/Test_EDC_2.pdf' )
        cnt = cnt + 1
        log.info('%s FileRead point %d' % ( method_name, cnt ))
        buffer = open('C:/PycharmProjects4/strage/Test_EDC_2.pdf', mode='rb').read()
        # レスポンスオブジェクト生成
        response = HttpResponse(buffer, content_type='application/pdf')  # PDFファイルを表す
        cnt = cnt + 1
        # ダウンロードファイル名設定
        log.info('%s ファイル名設定 point %d' % ( method_name, cnt ))
        response['Content-Disposition'] = 'attachment; filename="{fn}"'.format(fn=urllib.parse.quote("Test_EDC_2.pdf"))
        cnt = cnt + 1
    except Exception as e:
        print( e, 'error occurred')
        log.error( e )
        log.info('失敗')
    else:
        log.info('成功')
        return response
    finally:
        log.info('%s Close point %d' % ( method_name, cnt ))
        wb.Close(False)
        #excel.Workbooks(ExcelFileName).Close(SaveChanges=0)
        log.info('%s Quit point %d' % ( method_name, cnt ))
        excel.Quit()
        log.info('%s CoUninitialize point %d' % ( method_name, cnt ))
        pythoncom.CoUninitialize()  # Excelを終了した後はこれを呼び出す
        log.info(method_name + 'end')


