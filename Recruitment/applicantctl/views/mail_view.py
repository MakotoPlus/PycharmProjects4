from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import connection, transaction
from django.urls import reverse
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.urls import reverse_lazy
from applicantctl.models import T_Applicant_info,T_Judgment
from applicantctl.forms.mail_form import MailForm, MailFormSet

class MailView(LoginRequiredMixin, FormView):
    '''
    メール送信VIEW    
    '''
    template_name = "applicantctl/mail/mailview.html"
    subject_value = '応募者のご連絡'
    success_url = reverse_lazy('applicantctl:index')
    form_class = MailFormSet

    def get_context_data(self, **kwargs):
        '''templateに渡す contextを生成する

        パラメータのキーから、応募者情報を取得し
        self.app_info と context['app_info']に格納する

        親のget_context_data()を呼出して、form_classオブジェクトを初期化し

        context['form']にform_classを設定する。

        Parameters
        -------------------------
        **kwargs : dict

        Returns
        -------------------------
        dict
            templateに渡すdictを返す
        '''
        # 内部メソッドを呼んで、URLで指定されているキーを利用して
        # 該当データを取得する。
        #
        # 取得したデータは、'app_info'に設定する
        #  
        context = kwargs
        self.app_info_form = self.get_app_infor_form_object(**kwargs)        
        context['app_info'] = self.app_info_form
        #こいつで、プロパティのform_classが 設定された
        #contextが返って来る
        context = super().get_context_data(**kwargs)        
        return context

    def get_initial(self):
        """Return the initial data to use for forms on this view.

        self.app_info_formを利用して初期値を生成する

        self.app_info_formは、get_context_data()で設定している

        Parameters
        -------------------------
        Returns
        -------------------------

        Notes
        -------------------------
        このメソッドは、get, post両方で呼出される。

        get時(初期表示)は、subject, bodyに値を設定するが、

        post時は値を設定しないようにしている。

        判断方法は、selfにspp_infor_formが存在しているかで判断している。

        """
        initial = []
        if hasattr(self, 'app_info_form'):
            #件名設定
            subject = self.subject_value
            #本文設定
            body ='採用活動実施者各位 \n\n'     \
                'お疲れ様です。採用委員会からの連絡です。\n'    \
                '下記応募がありました。。本日より２営業日程度で書類選考を行い\n'    \
                '結果登録をお願い致します。\n'     \
                '尚、書類選考通過の場合は優先順位の高い部門が\n'  \
                '応募者へご連絡お願い致します。\n'    \
                '\n'    \
                '応募日:{0}\n'    \
                '応募者No:{1}\n'    \
                '応募者名:{2}\n'    \
                '経歴:{3}\n'    \
                '応募経路:{4}\n'    \
                '\n'    \
                '書類選考状況\n'    \
                '第1優先部:{5} 書類選考状況:{6} \n' \
                '第2優先部:{7} 書類選考状況:{8} \n' \
                '第3優先部:{9} 書類選考状況:{10} \n' \
                '\n'    \
                '以上よろしくお願い致します。'  \
                .format(self.app_info_form[1], self.app_info_form[2]    \
                ,self.app_info_form[3], self.app_info_form[4]   \
                ,self.app_info_form[5]
                ,self.app_info_form[6], self.app_info_form[7] if self.app_info_form[7] is not None else '検討中' \
                ,self.app_info_form[8], self.app_info_form[9] if self.app_info_form[9] is not None else '検討中' \
                ,self.app_info_form[10],self.app_info_form[11] if self.app_info_form[11] is not None else '検討中' 
            )
            initial = [{'subject':subject, 'body': body}]

        return initial

    def get_app_infor_form_object(self, **kwargs):
        '''
        MailView独自メソッド

        app_infoに設定する。応募者情報のオブジェクトを返す

        Parameters
        -----------------
        **kwargs dict
            リクエストパラメータ

        Returns
        -----------------
        tuple
            取得したデータ
        '''
        print(self.kwargs.get('pk'))
        sSql = '''
            select 
                APPL.key_applicant key_applicant
                ,APPL.applicant_date applicant_date
                ,APPL.applicant_no applicant_no
                ,APPL.applicant_name_text applicant_name_text
                ,M_Work_History.work_history_kbn work_history_kbn
                ,M_Appl_Route.appl_route_text appl_route_text
                ,M_Department_1.headquarters_text headquarters_1_text
                ,M_Judgment_1.judgment_text judgment_1_text
                ,M_Department_2.headquarters_text headquarters_2_text
                ,M_Judgment_2.judgment_text judgment_2_text
                ,M_Department_3.headquarters_text  headquarters_3_text
                ,M_Judgment_3.judgment_text judgment_3_text
                ,T_Judgment_1.key_judgment key_judgment_1
                ,T_Judgment_2.key_judgment key_judgment_2
                ,T_Judgment_3.key_judgment key_judgment_3
                ,M_Judgment_1.badge_text badge_text_1
                ,M_Judgment_2.badge_text badge_text_2
                ,M_Judgment_3.badge_text badge_text_3
            from 
                    (
                        (
                            (
                                (
                                    (
                                        (
                                            (
                                                (
                                                    (
                                                        (
                                                            (
                                                                T_Applicant_info AS APPL
                                                                left outer join T_Judgment As T_Judgment_1
                                                                ON APPL.key_applicant = T_Judgment_1.key_applicant_id AND T_Judgment_1.judgment_index=1 
                                                            )
                                                            left outer join T_Judgment As T_Judgment_2
                                                                ON APPL.key_applicant = T_Judgment_2.key_applicant_id AND T_Judgment_2.judgment_index=2 
                                                        )
                                                        left outer join T_Judgment As T_Judgment_3
                                                        ON APPL.key_applicant = T_Judgment_3.key_applicant_id AND T_Judgment_3.judgment_index=3 
                                                    )
                                                    left outer join M_Department as M_Department_1
                                                        ON T_Judgment_1.key_department_id = M_Department_1.key_index
                                                )
                                                left outer join M_Department as M_Department_2
                                                    ON T_Judgment_2.key_department_id = M_Department_2.key_index
                                            )
                                            left outer join M_Department as M_Department_3
                                                ON T_Judgment_3.key_department_id = M_Department_3.key_index
                                        )
                                        left outer join M_Judgment as M_Judgment_1
                                        ON T_Judgment_1.judgment_id = M_Judgment_1.key_judgment
                                    )
                                    left outer join M_Judgment as M_Judgment_2
                                    ON T_Judgment_2.judgment_id = M_Judgment_2.key_judgment
                                )
                                left outer  join M_Judgment as M_Judgment_3
                                ON T_Judgment_3.judgment_id = M_Judgment_3.key_judgment
                            )
                            inner join M_Work_History as M_Work_History
                            ON APPL.key_history_kbn_id = M_Work_History.key_history_kbn
                        )
                        inner join M_Appl_Route as M_Appl_Route
                        ON APPL.key_appl_route_id = M_Appl_Route.key_appl_route
                    )
                '''
        whereSql = ' WHERE APPL.key_applicant={0}'.format(self.kwargs.get('pk'))
        sSql = sSql + whereSql
        #print(sSql)
        cursor = connection.cursor()
        cursor.execute(sSql)
        rows = cursor.fetchall()
        print( type(rows[0]))
        return rows[0]

    def post(self, request, *args, **kwargs):
        #form = self.get_form()
        form = self.form_class(request.POST, request.FILES)
        #入力チェック
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)        


    def form_valid(self, form):
        '''
        入力チェックOK時に呼出されるメソッド

        '''
        self.send_mail(form)
        return super().form_valid(form)

    def send_mail(self, form):
        '''
        メール送信
        '''
        recipient_list = [
            settings.SEND_MAIL_ADRESS
        ]
        subject = form.cleaned_data[0]['subject']
        message = form.cleaned_data[0]['body']
        send_mail(subject, message, settings.SERVER_EMAIL, recipient_list)
        messages.info(self.request, 'メール送信しました。') 

