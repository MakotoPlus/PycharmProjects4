import datetime
from django.test import TestCase
from django.utils import timezone
from django.db import models
from django.db import connection

from .models import M_Appl_Route, M_Work_History, M_Department, T_Applicant_info, T_Judgment

class TestModel(TestCase):

    def setUp(self):
        #
        # 応募経路マスタ作成
        m_appl_route = M_Appl_Route.objects.create(
            #応募経路
            appl_route_text='マイナビ',
            u_user='usr'
        )

        #
        #業務経歴マスタ 作成
        m_work_history = M_Work_History.objects.create(
            work_history_kbn='未経験',
            u_user='usr'
        )
        
        #
        # 部マスタ作成
        m_department = M_Department.objects.create(
            headquarters_text ='SI第１本部',
            u_user='usr'
        )
        #応募者情報作成
        t_applicant_info_01 = T_Applicant_info.objects.create(
            applicant_date = timezone.now(),
            #応募経路
            key_appl_route = m_appl_route,
            #応募者№
            applicant_no = '10002',
            #応募者名
            applicant_name_text = '10002_応募者',
            #経歴区分KEY
            key_history_kbn = m_work_history,
            u_user='usr'
        )
        
        #応募者情報作成
        t_applicant_info = T_Applicant_info.objects.create(
            applicant_date = timezone.now(),
            #応募経路
            key_appl_route = m_appl_route,
            #応募者№
            applicant_no = '10001',
            #応募者名
            applicant_name_text = '10001_応募者',
            #経歴区分KEY
            key_history_kbn = m_work_history,
            u_user='usr'
        )
        #判定テーブル
        T_Judgment.objects.create(
            #部INDEX
            key_department = m_department,
            #応募者情報キー
            key_applicant = t_applicant_info,
            #優先順番
            judgment_index = '1',
            u_user='usr'
        )
        T_Judgment.objects.create(
            #部INDEX
            key_department = m_department,
            #応募者情報キー
            key_applicant = t_applicant_info,
            #優先順番
            judgment_index = '2',
            u_user='usr'
        )
        T_Judgment.objects.create(
            #部INDEX
            key_department = m_department,
            #応募者情報キー
            key_applicant = t_applicant_info,
            #優先順番
            judgment_index = '3',
            u_user='usr'
        )

    #-----------------------------------------------------------------
    # Modelでデータを取得するため別々のmodelオブジェクトのデータを取得する事は出来ない
    #-----------------------------------------------------------------
    def test_01(self):
        print( 'test_01' )
        tapplicants = T_Applicant_info.objects.raw('''
            select APPL.* from applicantctl_T_Applicant_info AS APPL
            left outer join applicantctl_T_Judgment As JUDG
                ON APPL.key_applicant = JUDG.key_applicant_id
            ''')
        print(tapplicants)
        for tapplicant in tapplicants:
            #print(tapplicant)
            print('応募者№[%s]応募者名[%s]' % (tapplicant.applicant_no, tapplicant.applicant_name_text))


    #-----------------------------------------------------------------
    # テーブルを結合してすべてのデータ列項目が取得出来る
    #-----------------------------------------------------------------
    def test_02(self):
        print( 'test_02' )
        cursor = connection.cursor()
        cursor.execute('''
            select APPL.*, JUDG.* from applicantctl_T_Applicant_info AS APPL
            left outer join applicantctl_T_Judgment As JUDG
                ON APPL.key_applicant = JUDG.key_applicant_id
            ''')
        rows = cursor.fetchall()
        for tapplicant in rows:
            print(type(tapplicant))
            print(type(tapplicant[0]))


