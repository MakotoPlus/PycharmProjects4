import logging
from django.db import connections
from django.db import reset_queries
from django.shortcuts import render
from django.http import HttpResponse

'''
    Middlewareクラス
    
    例外が発生した場合はロギングして、デフォルトのエラー画面へ遷移させる。
    
'''
class SimpleMiddleware:

    # ログStatic変数設定
    _log = logging.getLogger(__name__)
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    #---------------------------------------------------------------------
    # 例外発生時のHookメソッド
    #---------------------------------------------------------------------
    def process_exception(self, request, exception):
        self._log.exception(exception)
        content = {
            'error' : exception
        }
        #エラー画面へ遷移
        return render(request, 'applicantctl/err.html', content )

    def process_view(self, request, view_func, view_args, view_kwargs):
        #if view_func.__name__.startswith('api'):
        #    return HttpResponseBadRequest()
        #else:
        return None
