from django import forms
from django.forms.fields import DateField  
from django.conf import settings

#########################################
# メール送信フォーム
class MailSendForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    #    for field in self.fields.values():
    #        field.widget.attrs['class'] = 'form-control'
    #    self.fields['from_mail'].initial = settings.DEFAULT_FROM_EMAIL
    #    self.fields['from_mail'].widget.attrs['disabled'] = "disabled" 

    #from_mail = forms.EmailField(label='自分メールアドレス', required=False)
    to_mail = forms.EmailField(label='宛先メールアドレス')
    subject = forms.CharField(label='件名')
    mesage = forms.CharField(label='メッセージ', widget=forms.Textarea)


#MailSendFormSet = forms.formset_factory(MailSendForm, extra=1)

class TemplateMailSendForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    mail_choices = forms.fields.ChoiceField(
        choices = ( 
            ('1', '挨拶テンプレート'),
            ('2', '連絡テンプレート'),
            ('3', 'リマインドテンプレート')
        ),
        required=True,
        widget=forms.widgets.Select
    )

