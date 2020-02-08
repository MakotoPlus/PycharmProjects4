from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
#from django import forms
from django.forms import modelformset_factory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection, transaction
from django.http import HttpResponseRedirect
from ..util.logger import logger
from ..forms.SearchForm import SearchForm, SearchFormSet
import logging


log = logging.getLogger(__name__)

# Create your views here.
@login_required 
@logger(func_name="index_func")
def index_func(request):
    forms = SearchFormSet(request.GET or None)

    """
    GETパラメータのキー内容について。
    ページング処理のパラメータは、 'page'
    検索絞込み条件の'm_work_history','m_appl_route'の
    情報キーが存在した場合は、is_valid実施後にSQLのWhere句を生成する。
    """

    whereSql = ''
    
    #
    # パラメータに検索条件があるかチェックする
    # Request.GETからパラメータをリストに保存(lists)
    # タプルの中にタプルが格納されているので二重ループで、キー名の文字列が含まれているパラメータキーが存在するか
    # チェックし存在したらフラグをTrueに設定する。
    # １つあったらそれで十分なのでループを抜ける
    lists = request.GET.lists()
    is_m_appl_route_key = False     #検索条件パラメータ存在有無フラグ
    is_m_work_history_key = False   #検索条件パラメータ存在有無フラグ
    for tupls in lists:
        for key in tupls:
            if 'm_work_history' in key:
                is_m_work_history_key = True
                break
            elif 'm_appl_route' in key:
                is_m_appl_route_key = True
                break
        #どちらかのフラグがTrueとなったら終わり
        if is_m_appl_route_key or is_m_appl_route_key:
            break

    #
    # 1. パラメータに検索条件があったらSQL文のWHERE句を生成する。
    # 2. 検索パラメータが正常に作成されていない場合は下記エラーとなるため、新規にFormを生成する。
    #   「マネージメントフォームのデータが見つからないか、改竄されています。」
    #    これは検索条件なしでページ遷移パラメータが存在している場合に発生する。
    #
    if is_m_work_history_key or is_m_appl_route_key:
        if forms.is_valid() == True:
            for form in forms:
                if form.cleaned_data.get('m_appl_route'):
                    #print( 'm_appl_route=' + str(type(form.cleaned_data.get('m_appl_route'))))
                    whereSql = ' WHERE M_Appl_Route.key_appl_route =\'' + str(form.cleaned_data.get('m_appl_route').key_appl_route) + '\' '
                
                if form.cleaned_data.get('m_work_history'):
                    if whereSql:
                        whereSql = whereSql + ' AND '
                    else:
                        whereSql = ' WHERE '
                    whereSql = whereSql + 'M_Work_History.key_history_kbn=\'' + str(form.cleaned_data.get('m_work_history').key_history_kbn) + '\''
            #print( 'WHERE=[' + whereSql + ']' )
        else:
            #ありえないけと念のため
            forms = SearchFormSet(None)
    else:
        forms = SearchFormSet(None)

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
                                                	        applicantctl_T_Applicant_info AS APPL
                                                            left outer join applicantctl_T_Judgment As T_Judgment_1
                                                            ON APPL.key_applicant = T_Judgment_1.key_applicant_id AND T_Judgment_1.judgment_index=1 
                                                        )
                                                        left outer join applicantctl_T_Judgment As T_Judgment_2
                                                            ON APPL.key_applicant = T_Judgment_2.key_applicant_id AND T_Judgment_2.judgment_index=2 
                                                    )
                                                    left outer join applicantctl_T_Judgment As T_Judgment_3
                                                    ON APPL.key_applicant = T_Judgment_3.key_applicant_id AND T_Judgment_3.judgment_index=3 
                                                )
                                                left outer join applicantctl_M_Department as M_Department_1
                                                    ON T_Judgment_1.key_department_id = M_Department_1.key_index
                                            )
                                            left outer join applicantctl_M_Department as M_Department_2
                                                ON T_Judgment_2.key_department_id = M_Department_2.key_index
                                        )
                                        left outer join applicantctl_M_Department as M_Department_3
                                            ON T_Judgment_3.key_department_id = M_Department_3.key_index
                                    )
                                    left outer join applicantctl_M_Judgment as M_Judgment_1
                                    ON T_Judgment_1.judgment_id = M_Judgment_1.key_judgment
                                )
                                left outer join applicantctl_M_Judgment as M_Judgment_2
                                ON T_Judgment_2.judgment_id = M_Judgment_2.key_judgment
                            )
                            left outer  join applicantctl_M_Judgment as M_Judgment_3
                            ON T_Judgment_3.judgment_id = M_Judgment_3.key_judgment
                        )
                        inner join applicantctl_M_Work_History as M_Work_History
                        ON APPL.key_history_kbn_id = M_Work_History.key_history_kbn
                    )
                    inner join applicantctl_M_Appl_Route as M_Appl_Route
                    ON APPL.key_appl_route_id = M_Appl_Route.key_appl_route
                )
            '''
    sSql = sSql + whereSql
    sSql = sSql + ' ORDER BY applicant_date'


    cursor = connection.cursor()
    cursor.execute(sSql)
    rows = cursor.fetchall()
    page_obj = paginate_queryset( request, rows, 10 )

    #print( '-------------------------------------------------------------------' )
    #print( forms )
    context = {
        'forms' : forms,
         'list' : page_obj.object_list,
        'page_obj' : page_obj,
    }
    #print( context );
    return render(request, 'applicantctl/index.html', context)


def paginate_queryset(request, queryset, count):
    """Pageオブジェクトを返す。

    ページングしたい場合に利用してください。

    countは、1ページに表示する件数です。
    返却するPgaeオブジェクトは、以下のような感じで使えます。::

        {% if page_obj.has_previous %}
          <a href="?page={{ page_obj.previous_page_number }}">Prev</a>
        {% endif %}

    また、page_obj.object_list で、count件数分の絞り込まれたquerysetが取得できます。

    """
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj
