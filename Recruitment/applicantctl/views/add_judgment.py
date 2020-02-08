from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.forms import modelformset_factory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection, transaction
from django.http import HttpResponseRedirect
from ..util.logger import logger
from ..forms.JudgmentCreate_Form import JudgmenAdd_CreateFormSet
from ..forms.T_Judgment_Form import T_Judgment_Form
from ..models import T_Judgment, T_Applicant_info

#from ..forms import (
#    T_Applicant_infoForm, T_Applicant_infoCreateFormSet, SearchForm, SearchFormSet,
#    T_Judgment_Form, T_Judgment_CreateFormSet, JudgmentUpd_Form, Judgment_UpdateFormSet,
#    T_Applicant_infoUpdateFormSet, JudgmenAdd_CreateFormSet, JudgmentCreate_Form,
#    T_Applicant_info, M_Appl_Route, M_Work_History, T_Judgment
#    )

import logging
log = logging.getLogger(__name__)

#
# pk = 応募者情報.応募者情報キー
@logger(func_name="add_judgment_func")
@login_required 
def add_judgment_func(request, pk):
    # 応募者情報キーを使って判定テーブルにデータが存在するか確認
    #
    formset = JudgmenAdd_CreateFormSet(request.POST or None, queryset=T_Judgment.objects.filter(key_applicant=pk))
    message = ''

    if len(formset) < 3 :
        #
        # データが3件未満の場合は、存在件数＋新規登録で3件の入力フォームを作成する
        rformset = modelformset_factory(T_Judgment, form=T_Judgment_Form, extra=(3-(len(formset))))
        formset = rformset(request.POST or None, queryset=T_Judgment.objects.filter(key_applicant=pk))

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

        if is_dublicate_error == False:
            #エラーが発生していない場合はデータを保存する。
            # 保存前に修正対象FORM取得
            instances = formset.save(commit=False)
            print('instances=[%d] ' % len(instances))

            #
            # 更新対象FORMを取得して１件ずつコミットする
            for instance in instances:
                applicant_key = T_Applicant_info.objects.get(pk=pk)
                # 応募者情報キーを取得して設定
                instance.key_applicant = applicant_key
                instance.save()

            return HttpResponseRedirect(reverse('applicantctl:index'))
        else:
            # エラーメッセージ設定
            message = '優先順位を重複に設定出来ません'

    context = {
        'formset' : formset,
        'message' : message,
    }
    return render(request, 'applicantctl/add/judgment.html', context )
