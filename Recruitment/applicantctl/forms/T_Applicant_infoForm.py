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
# 応募者登録フォーム
class T_Applicant_infoForm(forms.ModelForm):

    # カレンダー表示テスト用の追加項目
    date_field = forms.DateField(
        label='追加日付項目',
        required = False,
        widget=datetimepicker.DatePickerInput(
            format='%Y/%m',
            options={
                'locale':'ja',
                'viewMode' : 'months'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        #更新日付項目は非表示、必須項目除外します。
        #更新、追加タイミングのmodel.saveメソッド時にシステム日付を設定します。
        self.fields['u_date'].widget = forms.HiddenInput()
        self.fields['u_date'].required = False

    class Meta:
        model = T_Applicant_info
        fields = ( 
            'applicant_date',
            'key_appl_route',
            'applicant_no',
            'applicant_name_text',
            'key_history_kbn',
            'u_date',
        )
        error_messages = {
            'applicant_no' : { 'required': '必須です!'
            },
            'applicant_name_text' : { 'required': '必須です!'
            }
        }
        widgets = {
            'applicant_date':datetimepicker.DatePickerInput(
                format='%Y/%m/%d',
                options={
                    'locale':'ja',
                }
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
