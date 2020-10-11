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
from applicantctl.forms.T_Applicant_infoForm import T_Applicant_infoCreateFormSet
from applicantctl.models import T_Applicant_info

import logging
log = logging.getLogger(__name__)

#@logger(func_name="add_func")
@login_required
def add_func(request):
    #新規Formしか不要な場合
    formset = T_Applicant_infoCreateFormSet(request.POST or None, queryset=T_Applicant_info.objects.none())
    #新規Formしか不要な場合(既存データも表示する場合)
    #formset = T_Applicant_infoCreateFormSet(request.POST or None)
    
    #応募経路マスタ, 業務経歴マスタ取得
    #list_m_appl_route = list(M_Appl_Route.objects.all())
    #t_list_1 = []
    #for r in list_m_appl_route:
    #    print('list_m_appl_route.key_appl_route [%d][%s]' % ( r.key_appl_route, r.appl_route_text))
    #    # キーと経路のタプル作成
    #    t_record = ( r.key_appl_route, r.appl_route_text)
    #    t_list_1.append(t_record)
    #
    #formset.fields['appl_route_text'].choices = t_list_1
    #
    print(formset.is_valid())
    if request.method == 'POST' and formset.is_valid():
        formset.save()
        return HttpResponseRedirect(reverse('applicantctl:index'))

    print('----------------------------')
    print(formset.errors)
    print(formset.is_valid())
    print('----------------------------')

    context = {
        'formset' : formset,
    }
    return render(request, 'applicantctl/add.html', context )
