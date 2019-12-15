from django import forms
from .models import T_Applicant_info, T_Judgment, M_Appl_Route, M_Work_History
#DJango用カレンダ
#from django.contrib.admin.widgets import AdminDateWidget

from django.forms.fields import DateField  
#from django.forms import extras
# BootStrap用カレンダ
import bootstrap_datepicker_plus as datetimepicker

#########################################
# 応募者登録フォーム
class T_Applicant_infoForm(forms.ModelForm):

    #
    #追加の場合はこれでOK
    #date_field = forms.DateField(
    #    widget=datetimepicker.DatePickerInput(format='%Y/%m/%d',)
    #    , label='追加日付項目'
    #)

    class Meta:
        model = T_Applicant_info
        fields = ( 
            'applicant_date',
             'key_appl_route',
            'applicant_no',
            'applicant_name_text',
           'key_history_kbn',
            )
        widgets = {
            'applicant_date':datetimepicker.DatePickerInput(
                format='%Y/%m/%d',
            ),

        }
        # DJango Adminカレンダー用
        #widgets = {
        #    'applicant_date':AdminDateWidget(),
        #    'date_field':AdminDateWidget(),
        #}
#モデルフォームセット
T_Applicant_infoCreateFormSet = forms.modelformset_factory(
    T_Applicant_info, form=T_Applicant_infoForm, extra=1)
    
T_Applicant_infoUpdateFormSet = forms.modelformset_factory(
    T_Applicant_info, form=T_Applicant_infoForm, extra=0)


#########################################
# 応募者検索フォーム
class SearchForm(forms.Form):
    #応募経路マスタ M_Appl_Route
    m_appl_route = forms.ModelChoiceField(queryset=M_Appl_Route.objects.all(), label='応募経路', required=False)
    #業務経歴マスタM_Work_History
    m_work_history = forms.ModelChoiceField(queryset=M_Work_History.objects.all(), label='業務経歴', required=False )
    
    def _init_(self, permission=None, *args, **kwargs ):
        super(SearchForm, self).__init__(*args,**kwargs)
        self.fields['m_appl_route'] = 'Tst'
    
    #def get_m_appl_route(self, permission):
    #    return M_Appl_Route.objects.all()

SearchFormSet = forms.formset_factory(SearchForm, extra=1)


#########################################
#
#判定テーブルフォーム
class T_Judgment_Form(forms.ModelForm):
    class Meta:
        model = T_Judgment
        fields = ( 
            'key_department',
            'judgment_index',
        )
#判定テーブルフォームセット
T_Judgment_CreateFormSet = forms.modelformset_factory(
    T_Judgment, form=T_Judgment_Form, extra=0)



#########################################
#
#書類選考更新フォーム
class JudgmentUpd_Form(forms.ModelForm):
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


#########################################
#
#書類選考新規登録用のフォーム
class JudgmentCreate_Form(forms.ModelForm):
    class Meta:
        model = T_Judgment
        fields = ( 
            'key_department',
            'judgment_index',
        )
        widgets = {
                    'key_applicant': forms.Select(attrs={ 'disabled':True,'required':False}),
                    'judgment_index': forms.Select(attrs={'readonly':True}),
        }
JudgmenAdd_CreateFormSet = forms.modelformset_factory(
    T_Judgment, form=JudgmentCreate_Form, extra=0)


