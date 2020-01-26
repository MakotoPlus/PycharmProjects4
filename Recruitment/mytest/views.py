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
import threading
import logging
import datetime

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
    ExcelFileName = 'C:/PycharmProjects4/strage/SAMPLE_ABC_EDC.xlsx'
    
    try:
        wb = excel.Workbooks.Open(ExcelFileName)
        
        #不要のシートを削除
        #sheets = ('【速報】稼働人数','12月スクランブル', '訪問管理','BP800戦略_定例会日程','Sample_コミュニケーション',)
        sheets = ('使用方法','FZ原価（解析）', '平成30年料金表（解析）','入力シート','原価_MW','入力シート (2)','原価（安全性）','Sheet1',)
        cnt = cnt + 1
        log.info('%s Sheet Delete point %d' % ( method_name, cnt ))
        for sheet in sheets:
            #log.info('%s Sheet [%s] Delete point %d' % ( method_name, sheet, cnt ))
            #wb.WorkSheets(sheet).Activate()
            #log.info('%s Sheet [%s] Delete point %d' % ( method_name, sheet, cnt ))
            #wb.WorkSheets(sheet).Delete()
            log.info('%s Sheet [%s] Visible:=False point %d' % ( method_name, sheet, cnt ))
            wb.WorkSheets(sheet).Visible = False


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


#
# Excel For PDF ファイルの実行Thread
def thread_excel_for_pdf(request):
    method_name ='thread_excel_for_pdf '
    log.info(method_name + 'start')
    cnt = 0
    cnt = cnt + 1

    #########################################################
    #
    # クラス：PDF作成スレッド
    # 概要：指定したExcelファイルを読込、不要シート名を削除して、PDFファイルを作成する
    #
    #########################################################
    class ThreadExcelPdf(threading.Thread):
        def __init__(self, *args, **kwds):
            threading.Thread.__init__( self )
            self.in_excel_filename = kwds['in_excel_filename']
            self.out_pdf_filename = kwds['out_pdf_filename']
            self.output_sheets = kwds['output_sheets']
        def run(self):
            try:
                cnt = 0
                log.info('%s point %d' % ( method_name, cnt ))
                #########################################################
                # COMのイニシャライズ(Excelを起動する前にこれを呼び出す)
                #########################################################
                pythoncom.CoInitialize()  
                excel = win32com.client.Dispatch("Excel.Application")
                #########################################################
                # Excel非表示設定
                #########################################################
                excel.Visible = False
                excel.DisplayAlerts = False
                cnt = cnt + 1
                log.info('%s OpenExcelFile[%s] point %d' % ( method_name, self.in_excel_filename, cnt ))
                wb = excel.Workbooks.Open(self.in_excel_filename, UpdateLinks=0, ReadOnly=True)
                cnt = cnt + 1
                log.info('%s Sheet Count[%d] point %d' % ( method_name, wb.Worksheets.Count, cnt ))
                #########################################################
                # シート名がPDF対象シート名か判断し、対象外の場合は一時削除用リストに格納する
                # 削除用リストに存在するシートは削除すると・・数式が壊れるので、非表示にして
                # PDF出力を行う！
                #########################################################
                list_delsheets = []
                if wb.Worksheets.Count > 0:
                    for index in range(1, wb.Worksheets.Count+1):
                        log.info( 'WORKSHEET=[' + wb.Worksheets(index).name + ']' )
                        #ワークシートが出力対象のシートか確認し対象でない場合は削除用リストへシート名追加
                        if False == (wb.Worksheets(index).name in self.output_sheets):
                            list_delsheets.append(wb.Worksheets(index).name)
                    # list_delsheets内にあるシートを全て非表示にする
                    for delsheet in list_delsheets:
                        log.info( 'WORKSHEET=[' + delsheet + '] Set Visible=False' )
                        #wb.WorkSheets(delsheet).Delete()
                        wb.WorkSheets(delsheet).Visible = False

                #########################################################
                # 出力ファイル名が存在したらファイル名を変更する
                #
                #########################################################
                out_file = self.out_pdf_filename
                plex = 0
                while ( False != os.path.isfile( out_file + '.dmy')) :
                    log.info('%s File Change[%s] point %d' % ( method_name, out_file + '.dmy', cnt ))
                    plex = plex + 1
                    out_file =  self.out_pdf_filename + '(' + str(plex) + ')'

                #ダミーファイルを出力
                with open(out_file + ".dmy", mode='w') as f:
                    f.write(out_file)


                #if os.path.isfile(self.out_pdf_filename):
                #    #ファイル削除
                #    log.info('%s File Remove[%s] point %d' % ( method_name, self.out_pdf_filename, cnt ))
                #    os.remove(self.out_pdf_filename)

                cnt = cnt + 1
                log.info('%s Sheet PDF Export point %d' % ( method_name, cnt ))
                #########################################################
                # PDF出力
                #########################################################
                wb.ExportAsFixedFormat(0, out_file + '.pdf' )
                #########################################################
                # Excelクローズ処理
                #########################################################
                wb.Close(False)
                cnt = cnt + 1
                log.info('%s Quit point %d' % ( method_name, cnt ))
                excel.Quit()
            except Exception as e:
                print( e, 'error!!')
                log.error( e )
                log.info('失敗')
            #else:
            #    log.info('成功')
            #    #return response
            finally:
                log.info('%s CoUninitialize point %d' % ( method_name, cnt ))
                pythoncom.CoUninitialize()  # Excelを終了した後はこれを呼び出す
                log.info('%s Thread End' % ( method_name ))

    #########################################################
    #スレッドパラメータ作成
    #########################################################
    # Input ExcelFile名
    in_excel_filename='C:/PycharmProjects4/strage/SAMPLE_ABC_EDC.xlsx'
    # Output PdfFile名
    out_pdf_filename='C:/PycharmProjects4/strage/SAMPLE_ABC_EDC'
    #PDF化シート名
    output_sheets = ('総合表紙（SP用）','表紙（Pモニ）','内訳（Pモニ）','前提（Pモニ）','表紙（契約）','内訳（契約）','前提（契約）','表紙（登録DM）','内訳（登録DM)',
                '前提（登録DM)','表紙（解析）','前提（解析）','表紙（MW)','内訳（MW)','表紙(安全性)',)
    
    
    #########################################################
    #スレッド起動
    #########################################################
    thread = ThreadExcelPdf(in_excel_filename=in_excel_filename, 
                            out_pdf_filename=out_pdf_filename,
                            output_sheets=output_sheets
                            )
    thread.start()
    now = datetime.datetime.now()
    context = {
        'msg' : 'PDF処理実行しました。結果はのちほど(' + str(now) + ')'
    }
    log.info('index end')
    return render(request, 'mytest/index.html', context)
