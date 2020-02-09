from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.db import transaction
from ..util.logger import logger
from ..forms.JudgmentUpd_Form import JudgmentUpd_Form
from ..models import T_Judgment
import logging
log = logging.getLogger(__name__)


#####################################################
# 更新画面
class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = T_Judgment
    form_class = JudgmentUpd_Form
    template_name = "applicantctl/upd/judgment.html"
    #, args=(model.key_judgment,)
    success_url = reverse_lazy('applicantctl:index',)

