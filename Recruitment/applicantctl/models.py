from django.db import models
from django.utils import timezone

# Create your models here.

#判定マスタ
class M_Judgment(models.Model):
    #判定値
    key_judgment = models.AutoField(primary_key=True)
    #判定内容
    judgment_text = models.CharField(max_length=100, verbose_name='判定内容')
    #更新者
    u_user = models.CharField(max_length=100, verbose_name='更新者')
    #更新日
    u_date = models.DateTimeField(verbose_name='更新日時',auto_now=True)
    def __str__(self):
        return self.judgment_text




#応募経路マスタ
class M_Appl_Route(models.Model):
    #応募経路KEY
    key_appl_route = models.AutoField(primary_key=True)
    #応募経路
    appl_route_text = models.CharField(max_length=200, verbose_name='応募経路')
    #更新者
    u_user = models.CharField(max_length=100, verbose_name='更新者')
    #更新日
    u_date = models.DateTimeField(verbose_name='更新日時',auto_now=True)
    def __str__(self):
        return self.appl_route_text

#業務経歴マスタ
class M_Work_History(models.Model):
    #経歴区分KEY
    key_history_kbn = models.AutoField(primary_key=True)
    #経歴区分
    work_history_kbn = models.CharField(max_length=100, verbose_name='経歴区分')
    #更新者
    u_user = models.CharField(max_length=100, verbose_name='更新者')
    #更新日
    u_date = models.DateTimeField(verbose_name='更新日時',auto_now=True)
    def __str__(self):
        return self.work_history_kbn

#部マスタ
class M_Department(models.Model):
    #部INDEX
    key_index = models.AutoField(primary_key=True, null=False)
    #本部名
    headquarters_text = models.CharField(max_length=100, verbose_name='本部')
    #部署名
    #deparment_text = models.CharField(unique=True, max_length=100, verbose_name='部')
    #更新者
    u_user = models.CharField(max_length=100, verbose_name='更新者')
    #更新日
    u_date = models.DateTimeField(verbose_name='更新日時',auto_now=True)
    def __str__(self):
        return self.headquarters_text

#応募者情報
class T_Applicant_info(models.Model):
    #応募者情報キー
    key_applicant = models.AutoField(primary_key=True)
    #応募日
    applicant_date = models.DateField(verbose_name='応募日')
    #応募経路KEY
    # key_appl_route = models.IntegerField(null=True,verbose_name='応募経路')
    key_appl_route = models.ForeignKey(M_Appl_Route, null=True, on_delete=models.PROTECT,verbose_name='応募経路')

    #応募者№
    applicant_no = models.CharField(max_length=20, verbose_name='応募者No')
    #応募者名
    applicant_name_text = models.CharField(max_length=100, verbose_name='応募者名')
    #経歴区分KEY
    #key_history_kbn = models.IntegerField(null=True,verbose_name='経歴区分')
    key_history_kbn = models.ForeignKey(M_Work_History, null=True, on_delete=models.PROTECT,verbose_name='経歴区分')
    #更新者
    u_user = models.CharField(max_length=100, verbose_name='更新者')
    #更新日
    #u_date = models.DateTimeField(verbose_name='更新日時',auto_now=True, default=timezone.now)
    u_date = models.DateTimeField(verbose_name='更新日時', default=timezone.now)
    
    def __str__(self):
        return self.applicant_name_text

    def save(self, *args, **kwargs):
        self.u_date = timezone.now()
        super().save(*args, **kwargs)


#判定テーブル
class T_Judgment(models.Model):
    #
    CONST_JUDGMENT_INDEX = (( 1, '1'), (2, '2'), (3, '3'))
    #判定テーブルキー
    key_judgment = models.AutoField(primary_key=True)
    #部INDEX
    key_department = models.ForeignKey(M_Department, null=False, on_delete=models.PROTECT, verbose_name='本部')
    #応募者情報キー
    key_applicant = models.ForeignKey(T_Applicant_info, null=False, on_delete=models.CASCADE, verbose_name='応募者情報Key')
    #優先順番
    judgment_index = models.IntegerField(null=False, verbose_name='優先順位', choices=CONST_JUDGMENT_INDEX)
    #判定
    judgment = models.ForeignKey(M_Judgment, null=True, on_delete=models.PROTECT, verbose_name='面談実施判定')
    #更新者
    u_user = models.CharField(max_length=100, verbose_name='更新者')
    #更新日
    u_date = models.DateTimeField(verbose_name='更新日時',auto_now=True)
    def __str__(self):
        return str(self.key_judgment)

