from django import forms
from django.utils import timezone

#DJango用カレンダ
#from django.contrib.admin.widgets import AdminDateWidget
from ..models import T_Applicant_info, T_Judgment, M_Appl_Route, M_Work_History

from django.forms.fields import DateField  
#from django.forms import extras
# BootStrap用カレンダ
import bootstrap_datepicker_plus as datetimepicker


#########################################
#
#書類選考新規登録用のフォーム
class JudgmentCreate_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['u_date'].widget = forms.HiddenInput()
        self.fields['u_date'].required = False
        #self.fields['key_judgment'].widget = forms.HiddenInput()
        #self.fields['key_judgment'].required = False

    class Meta:
        model = T_Judgment
        fields = ( 
            'key_judgment',
            'key_department',
            'judgment_index',
            'u_date',
        )
        widgets = {
                    'key_applicant': forms.Select(attrs={ 'disabled':True,'required':False}),
                    'judgment_index': forms.Select(attrs={'readonly':True}),
        }
        #def save(self, *args, **kwargs):
        #    print("保存処理来たよ！")
        #    self.u_date = timezone.now()
        #    super().save(*args, **kwargs)

    #def save(self, *args, **kwargs):
    #    print("保存処理来たよ！！")
    #    #self.u_date = timezone.now()
    #    super().save(*args, **kwargs)

JudgmenAdd_CreateFormSet = forms.modelformset_factory(
    T_Judgment, form=JudgmentCreate_Form, extra=0)


