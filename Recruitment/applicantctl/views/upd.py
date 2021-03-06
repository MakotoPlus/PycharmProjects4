from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
#from django import forms
from django.forms import modelformset_factory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection, transaction
from django.http import HttpResponseRedirect
from applicantctl.util.logger import logger
from applicantctl.forms.T_Applicant_infoForm import T_Applicant_infoUpdateFormSet, T_Applicant_infoForm
from applicantctl.models import T_Applicant_info

import logging
log = logging.getLogger(__name__)

#@logger(func_name="upd_func")
@login_required 
@transaction.atomic
def upd_func(request, pk):
    #楽観ロックなので更新日を設定する
    record = T_Applicant_info.objects.select_for_update().get(pk=pk)
    record_u_date = record.u_date
    errmsg = ''
    if request.method == 'POST':
        log.debug('POST----------------------------')
        form = T_Applicant_infoForm(request.POST, instance=record)
        if form.is_valid():
            print( 'SAVE!!')
            #recordの更新バージョンとformの更新バージョンを比較する
            log.debug( "is valid After form.cleaned_u_data=[%s]" % str(form.cleaned_data['u_date']))
            if record_u_date != form.cleaned_data['u_date']:
                log.error( "不整合発生!![%s][%s]" %  (str(record_u_date), str(form.cleaned_data['u_date'])))
                errmsg = '他のユーザが更新された可能性があります。一度画面を戻って再度実行して下さい'
            else:
                #更新カウンターインクリメント
                form.save()
                return HttpResponseRedirect(reverse('applicantctl:index'))
    else:
        log.debug('NOT POST----------------------------')
        form = T_Applicant_infoForm(instance=record)
    context = {
        'form' : form,
        'errmsg' : errmsg,
        'key_applicant': pk,
    }
    return render(request, 'applicantctl/upd.html', context )
