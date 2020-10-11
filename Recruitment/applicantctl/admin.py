from django.contrib import admin
from applicantctl.models import 	\
	M_Appl_Route, M_Work_History, M_Department, 	\
	M_Judgment, M_Appl_Status

# Register your models here.

#クラス宣言
class M_Appl_RouteAdmin(admin.ModelAdmin):
	list_display = ('key_appl_route', 'appl_route_text')
class M_Work_HistoryAdmin(admin.ModelAdmin):
	list_display = ('key_history_kbn', 'work_history_kbn')
class M_DepartmentAdmin(admin.ModelAdmin):
	list_display = ('key_index', 'headquarters_text')
class M_JudgmentAdmin(admin.ModelAdmin):
	list_display = ('key_judgment', 'judgment_text', 'badge_text')
class M_Appl_StatusAdmin(admin.ModelAdmin):
	list_display = ('appl_status_kbn', 'status_text')

admin.site.register(M_Appl_Route, M_Appl_RouteAdmin) #決まった書き方
admin.site.register(M_Work_History, M_Work_HistoryAdmin) #決まった書き方
admin.site.register(M_Department, M_DepartmentAdmin) #決まった書き方
admin.site.register(M_Judgment, M_JudgmentAdmin) #決まった書き方
admin.site.register(M_Appl_Status, M_Appl_StatusAdmin) #決まった書き方

