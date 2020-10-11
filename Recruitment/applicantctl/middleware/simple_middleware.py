import logging
from django.db import connections
from django.db import reset_queries
from django.shortcuts import render
from django.http import HttpResponse

class SimpleMiddleware:
    '''
    Middlewareクラス
    
    例外が発生した場合はロギングして、デフォルトのエラー画面へ遷移させる。
    
    '''

    
    def __init__(self, get_response):
        '''
        サーバ起動時に一度だけ呼び出されるメソッド

        parameters
        -------------------------
        get_respoinse : 

        '''
        self._log = logging.getLogger(__name__)
        self.get_response = get_response

    def __call__(self, request):
        '''
        リクエスト毎に呼び出されるメソッド

        Parameters
        -------------------------
        request : 
        '''

        # 呼出し前
        response = self.get_response(request)
        # 呼出し後
        return response

    def process_exception(self, request, exception):
        '''
        例外発生時のHookメソッド

        '''

        self._log.exception(exception)
        content = {
            'error' : exception
        }
        #エラー画面へ遷移
        return render(request, 'applicantctl/err.html', content )

    def process_view(self, request, view_func, view_args, view_kwargs):
        '''
        view関数を呼び出す直前にhookされるメソッド

        __call__(self, request)　との違い

        実行されるview関数, そのview関数への引数（例えばurlsで定義したパラメータ）

        を知っているのが特徴です。
        Parameters
        -------------------------
        request : 

        Returns
        -------------------------
        None
            そのままview関数への処理が進む
        HttpResponse
            処理はここで止まり、サーバからの
            レスポンスとしてその HttpResponse で定義された内容が返ります。

        '''
        self._log.info('request:{0}args{1}kwargs{2}'.format(request,view_args,view_kwargs))

        return None
