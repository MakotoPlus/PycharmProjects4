from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.forms import modelformset_factory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection, transaction
from django.http import HttpResponseRedirect
from applicantctl.util.logger import logger
from applicantctl.forms.JudgmentCreate_Form import JudgmenAdd_CreateFormSet
from applicantctl.forms.T_Judgment_Form import T_Judgment_Form
from applicantctl.models import T_Judgment, T_Applicant_info
from datetime import datetime, timedelta
from django.utils import timezone
from applicantctl.util.original_exception import OriginalException


import logging
log = logging.getLogger(__name__)

#
# pk = 応募者情報.応募者情報キー
# @logger(func_name="add_judgment_func")
@login_required 
@transaction.atomic
def add_judgment_func(request, pk):
    message = ''
    rformset = modelformset_factory(T_Judgment, form=T_Judgment_Form, extra=3, max_num=3)
    #現在の登録件数を取得して、優先順位の初期値を設定する
    records = T_Judgment.objects.filter(key_applicant=pk)
    init_cnt = 0 if records is None else len(records)
    judgment_inital = [{'judgment_index':init_cnt + 1},{'judgment_index':init_cnt + 2},{'judgment_index':init_cnt + 3}]
    formset = rformset(request.POST or None,    \
                initial=judgment_inital,        \
                queryset=T_Judgment.objects.filter(key_applicant=pk))

    if request.method == 'POST' and formset.is_valid():
        # DEBUG
        print( '保存じっこう')
        #
        #
        # １～３で入力されたFORMの優先順位が１，２，３が重複登録されていないかチェックする。
        # 通常のFORM内の入力チェックはFormオブジェクトで行うべきだが今回のようなチェックはどこで行うか
        # 不明なためここでチェックを行う。
        #
        # formsetオブジェクトもうまくアクセスできないので cleaned_data['']という謎の箇所から
        # アクセスしてデータ入力チェックを行う。
        judgment_index_check = []
        is_dublicate_error = False
        for frm in formset:
            if 'judgment_index' in frm.cleaned_data:
                if frm.cleaned_data['judgment_index'] in judgment_index_check:
                    # 既に値があったら重複入力
                    is_dublicate_error = True
                else:
                    judgment_index_check.append( frm.cleaned_data['judgment_index'] )
        is_update_ok = True
        if is_dublicate_error == False:
            #エラーが発生していない場合はデータを保存する。
            # 保存前に修正対象FORM取得
            instances = formset.save(commit=False)
            print('instances=[%d] ' % len(instances))
            applicant_key = T_Applicant_info.objects.get(pk=pk)
            #print('applicant_key=[%d] ' % (applicant_key.key_applicant))
            #
            # 更新対象FORMを取得して１件ずつコミットする
            for instance in instances:
                # 応募者情報キーを取得して設定
                instance.key_applicant = applicant_key
                if instance.key_judgment is None:
                    log.info( "Save u_date=[%s]" % (str(instance.u_date)))
                else:
                    #log.info( "Save key=[%d]u_date=[%s]" % (instance.key_judgment, str(instance.u_date)))
                    #
                    # key_judgmentが存在するという事は、Updateであるので楽観ロック実行する。
                    # 1.行ロック
                    judg_Record = T_Judgment.objects.select_for_update().get(pk=instance.key_judgment)
                    # 2.更新日比較
                    now = datetime.now()
                    print(now.strftime('%Y/%m/%d %H:%M:%S'))
                    log.info( "pk=[%d] Db.u_date=[%s] Form.u_date[%s]" % 
                        (instance.key_judgment, (judg_Record.u_date).strftime('%Y/%m/%d %H:%M:%S'), 
                        instance.u_date.strftime('%Y/%m/%d %H:%M:%S')))
                    if judg_Record.u_date == instance.u_date:
                        log.info( "更新日付一致Ok")
                    else:
                        #日付が一致しなかった場合はUpdateフラグをFalseに設定
                        is_update_ok = False
                        log.info( "更新日付不一致")
            if is_update_ok:
                # 問題なければ保存
                #for instance in instances:
                #    print("保存")
                #    instance.save()
                formset.save()
                return HttpResponseRedirect(reverse('applicantctl:index'))
            message = "既に別のユーザに更新されました。再度実行して下さい"
        else:
            # エラーメッセージ設定
            message = '優先順位を重複に設定出来ません'

    context = {
        'formset' : formset,
        'message' : message,
    }
    return render(request, 'applicantctl/add/judgment.html', context )
