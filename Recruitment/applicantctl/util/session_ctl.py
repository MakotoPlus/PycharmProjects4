import logging
#from django.db import connections
#from django.db import reset_queries
#from django.shortcuts import render

#
# session_ctl
# パラメータ：session_ctl_args (保持するセッション名)
# 
#
# 概要：パラメータで指定された保持するセッション名を指定する
#       保持対象となるのは、指定したセッション名と前方一致したセッション名
#       一致しなかったセッション名は削除される。
#       但し、Django用の先頭名が '_'のものは削除しない
#
def session_ctl(*session_ctl_args):
    def __decorator(func):
        def inner(*args, **kwargs):
            # 第一パラメータのrequestオブジェクトを取得
            request = args[0]
            dellist =[]
            #
            # 保持しているセッション名から削除すべき
            # セッションKey名をdellistに保存する
            #
            for key in request.session.keys():
                if False == key.startswith('_'):
                    # _ で始まらない場合
                    # Session保持としてパラメータ指定されている名前か確認する
                    # 名前は複数も想定し完全一致ではなく先頭一致していれば
                    # 保持とみなす
                    bret = False
                    for session_ctl_key in session_ctl_args:
                        bret = key.startswith(session_ctl_key)
                        if bret:
                            break
                    if bret == False:
                        #一致しなかった場合はセッションを保存
                        #print( 'delete key[%s]' % key )
                        dellist.append(key)
                    else:
                        #print( 'NOT delete key[%s]' % key )
                        pass
                else:
                    #print( 'nodelete_key[%s]' % key )
                    pass
            #print( dellist )
            #削除処理
            for delkey in dellist:
                #print( 'del key[%s]' % delkey )
                del request.session[delkey]
            #関数呼び出し
            result = func(*args, **kwargs)
            return result
        return inner
    return __decorator
