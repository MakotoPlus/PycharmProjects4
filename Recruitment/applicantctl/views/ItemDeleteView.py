from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction
from ..util.logger import logger
from ..forms.JudgmentUpd_Form import JudgmentUpd_Form
from ..models import T_Applicant_info, T_Judgment
import logging
log = logging.getLogger(__name__)


#####################################################
# 応募情報削除
class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = T_Applicant_info
    success_url = reverse_lazy('applicantctl:index',)
