#
# メール送信フォーム
#
#
from django import forms


class MailForm(forms.Form):
    '''
    メール送信Form
    '''
    subject = forms.CharField(label='件名', max_length=100, required=True, help_text='最大100文字')
    body = forms.CharField(label='本文', required=True, widget=forms.Textarea(attrs={'rows':'25'}))

MailFormSet = forms.formset_factory(MailForm, extra=0)