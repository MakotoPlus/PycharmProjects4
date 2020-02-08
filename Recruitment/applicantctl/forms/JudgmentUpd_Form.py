from django import forms
from django.utils import timezone
from ..models import T_Applicant_info, T_Judgment, M_Appl_Route, M_Work_History

#DJango用カレンダ
#from django.contrib.admin.widgets import AdminDateWidget

from django.forms.fields import DateField  

#########################################
#
#書類選考更新フォーム
class JudgmentUpd_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = T_Judgment
        fields = ( 
            'judgment',
            'key_judgment',
        )
        widgets = {
        }
#書類選考テーブルフォームセット
Judgment_UpdateFormSet = forms.modelformset_factory(
    T_Judgment, form=JudgmentUpd_Form, extra=0)
