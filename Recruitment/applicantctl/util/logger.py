import logging
from django.db import connections
from django.db import reset_queries

def logger(func_name):
    def __decorator(func):
        def inner(*args, **kwargs):
            log = logging.getLogger(__name__)
            log.info(func_name + "() 開始")
            #今まで実行していたSQLをクリア
            reset_queries()
            #実際のメソッド呼出し
            result = func(*args, **kwargs)
            #今まで実行していたSQLをログへ出力
            log.debug(connections['default'].queries)
            log.info(func_name + "() 終了")
            return result
        return inner
    return __decorator
