from django import forms
from django.utils import timezone
from ..models import T_Applicant_info, T_Judgment, M_Appl_Route, M_Work_History

#DJango用カレンダ
#from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField  


#########################################
# 応募者検索フォーム
class SearchForm(forms.Form):
    #応募経路マスタ M_Appl_Route
    m_appl_route = forms.ModelChoiceField(queryset=M_Appl_Route.objects.all(), label='応募経路', required=False, )
    #業務経歴マスタM_Work_History
    m_work_history = forms.ModelChoiceField(queryset=M_Work_History.objects.all(), label='業務経歴', required=False )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
    
    #def get_m_appl_route(self, permission):
    #    return M_Appl_Route.objects.all()

SearchFormSet = forms.formset_factory(SearchForm, extra=1)

