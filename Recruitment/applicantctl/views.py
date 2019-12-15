from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse
from .forms import T_Applicant_infoForm, T_Applicant_infoCreateFormSet, SearchForm, SearchFormSet
from .forms import T_Judgment_Form, T_Judgment_CreateFormSet, JudgmentUpd_Form, Judgment_UpdateFormSet, T_Applicant_infoUpdateFormSet, JudgmenAdd_CreateFormSet, JudgmentCreate_Form
from .models import T_Applicant_info, M_Appl_Route, M_Work_History, T_Judgment
from django import forms
from django.forms import modelformset_factory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

# Create your views here.
@login_required 
def index(request):

    forms = SearchFormSet(request.GET or None)

    """
    GETパラメータのキー内容について。
    ページング処理のパラメータ 'page'
    検索絞込み条件の'm_work_history','m_appl_route'の情報は
    'form-0-m_appl_route','form_0-m_work_history'というキー値となっているので
    存在するかの確認は、完全一致ではなく部分一致で確認する
    キーが存在した場合は、isValid実施後にSQLのWhere句を生成する。
    
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

    cursor = connection.cursor()
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


    #print( sSql )
    cursor.execute(sSql)
    rows = cursor.fetchall()
    page_obj = paginate_queryset( request, rows, 3 )

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



@login_required
def add(request):
    #新規Formしか不要な場合
    formset = T_Applicant_infoCreateFormSet(request.POST or None, queryset=T_Applicant_info.objects.none())
    #新規Formしか不要な場合(既存データも表示する場合)
    #formset = T_Applicant_infoCreateFormSet(request.POST or None)
    
    #応募経路マスタ, 業務経歴マスタ取得
    #list_m_appl_route = list(M_Appl_Route.objects.all())
    #t_list_1 = []
    #for r in list_m_appl_route:
    #    print('list_m_appl_route.key_appl_route [%d][%s]' % ( r.key_appl_route, r.appl_route_text))
    #    # キーと経路のタプル作成
    #    t_record = ( r.key_appl_route, r.appl_route_text)
    #    t_list_1.append(t_record)
    #
    #formset.fields['appl_route_text'].choices = t_list_1
    #
    if request.method == 'POST' and formset.is_valid():
        formset.save()
        return HttpResponseRedirect(reverse('applicantctl:index'))

    context = {
        'formset' : formset,
    }
    return render(request, 'applicantctl/add.html', context )


@login_required 
def upd(request, pk ):
    formset = T_Applicant_infoUpdateFormSet(request.POST or None, queryset=T_Applicant_info.objects.filter(key_applicant=pk))


    if request.method == 'POST' and formset.is_valid():
        formset.save()
        return HttpResponseRedirect(reverse('applicantctl:index'))

    context = {
        'formset' : formset,
        'key_applicant': pk,
    }
    return render(request, 'applicantctl/upd.html', context )
#
# pk = 応募者情報.応募者情報キー
@login_required 
def add_judgment(request, pk ):

    # 応募者情報キーを使って判定テーブルにデータが存在するか確認
    #
    formset = JudgmenAdd_CreateFormSet(request.POST or None, queryset=T_Judgment.objects.filter(key_applicant=pk))
    message = ''

    if len(formset) < 3 :
        #
        # データが3件未満の場合は、存在件数＋新規登録で3件の入力フォームを作成する
        rformset = forms.modelformset_factory(T_Judgment, form=T_Judgment_Form, extra=(3-(len(formset))))
        formset = rformset(request.POST or None, queryset=T_Judgment.objects.filter(key_applicant=pk))

    if request.method == 'POST' and formset.is_valid():
        # DEBUG
        print( '保存じっこう')
        #
        #
        # １～３で入力されたFORMの優先順位が１，２，３が重複登録されていないかチェックする。
        # 通常のFORM内の入力チェックはFormオブジェクトで行うべきだが今回のようなチェックはどこで行うか
        # 不明なためここでチェックを行う。
        #
        # formsetオブジェクトもうまくアクセスできないので cleaned_data['']という謎の箇所から
        # アクセスしてデータ入力チェックを行う。
        judgment_index_check = []
        is_dublicate_error = False
        for frm in formset:
            if 'judgment_index' in frm.cleaned_data:
                if frm.cleaned_data['judgment_index'] in judgment_index_check:
                    # 既に値があったら重複入力
                    is_dublicate_error = True
                else:
                    judgment_index_check.append( frm.cleaned_data['judgment_index'] )

        if is_dublicate_error == False:
            #エラーが発生していない場合はデータを保存する。
            # 保存前に修正対象FORM取得
            instances = formset.save(commit=False)
            print('instances=[%d] ' % len(instances))

            #
            # 更新対象FORMを取得して１件ずつコミットする
            for instance in instances:
                applicant_key = T_Applicant_info.objects.get(pk=pk)
                # 応募者情報キーを取得して設定
                instance.key_applicant = applicant_key
                instance.save()
            return HttpResponseRedirect(reverse('applicantctl:index'))
        else:
            # エラーメッセージ設定
            message = '優先順位を重複に設定出来ません'

    context = {
        'formset' : formset,
        'message' : message,
    }
    return render(request, 'applicantctl/add/judgment.html', context )

#####################################################
# 更新画面
class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = T_Judgment
    form_class = JudgmentUpd_Form
    template_name = "applicantctl/upd/judgment.html"
    #, args=(model.key_judgment,)
    success_url = reverse_lazy('applicantctl:index',)

#####################################################
# 応募情報削除
class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = T_Applicant_info
    success_url = reverse_lazy('applicantctl:index',)
