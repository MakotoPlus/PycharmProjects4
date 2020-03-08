import logging
from django.db import connections
from django.db import reset_queries
from django.shortcuts import render

def logger(func_name):
    def __decorator(func):
        def inner(*args, **kwargs):
            log = logging.getLogger(__name__)
            log.info(func_name + "() 開始")
            #今まで実行していたSQLをクリア
            reset_queries()
            try:
                #実際のメソッド呼出し
                result = func(*args, **kwargs)
            except Exception  as e:
                #とりあえずSQLは出力する
                sql_list = connections['default'].queries
                for sql in sql_list:
                    #今まで実行していたSQLをログへ出力
                    log.debug(sql)
                #例外情報ログ出力
                log.exception(e)
                log.info(func_name + "() 終了")
                #例外が発生したらエラー画面へ遷移
                content = {
                    'error' : e
                }
                #エラー画面へ遷移
                return render(args[0], 'applicantctl/err.html', content )
            sql_list = connections['default'].queries
            for sql in sql_list:
                #今まで実行していたSQLをログへ出力
                log.debug(sql)
            log.info(func_name + "() 終了")
            return result
        return inner
    return __decorator
