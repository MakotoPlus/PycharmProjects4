from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction
from .util.logger import logger
from .forms import JudgmentUpd_Form
from .models import T_Applicant_info, T_Judgment
from .viewfunc.index import index_func
from .viewfunc.add import add_func
from .viewfunc.upd import upd_func
from .viewfunc.add_judgment import add_judgment_func

import logging
log = logging.getLogger(__name__)

# Create your views here.
@login_required 
@logger(func_name="index")
def index(request):
    return index_func(request)


@logger(func_name="add")
@login_required
def add(request):
    return add_func(request)

@logger(func_name="upd")
@login_required 
@transaction.atomic
def upd(request, pk ):
    return upd_func(request, pk)

#
# pk = 応募者情報.応募者情報キー
@logger(func_name="add_judgment")
@login_required 
def add_judgment(request, pk ):
    return add_judgment_func(request, pk )

#####################################################
# 更新画面
class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = T_Judgment
    form_class = JudgmentUpd_Form
    template_name = "applicantctl/upd/judgment.html"
    #, args=(model.key_judgment,)
    success_url = reverse_lazy('applicantctl:index',)

#####################################################
# 応募情報削除
class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = T_Applicant_info
    success_url = reverse_lazy('applicantctl:index',)
