from django import forms
from django.utils import timezone
from ..models import T_Applicant_info, T_Judgment, M_Appl_Route, M_Work_History

#DJango用カレンダ
#from django.contrib.admin.widgets import AdminDateWidget

from django.forms.fields import DateField  
#from django.forms import extras
# BootStrap用カレンダ
import bootstrap_datepicker_plus as datetimepicker


#########################################
#
#判定テーブルフォーム
class T_Judgment_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = T_Judgment
        fields = ( 
            'key_department',
            'judgment_index',
        )
#判定テーブルフォームセット
T_Judgment_CreateFormSet = forms.modelformset_factory(
    T_Judgment, form=T_Judgment_Form, extra=0)
