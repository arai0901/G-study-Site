from django.db import models
from django.contrib.auth.models import User
from accounts.models import CustomUser
from django import forms

# 会員マスタ
class Kaiin(models.Model):
    class Meta:
        db_table = 'kaiin'

    name = models.CharField('会員名', max_length=255, null=True, blank=True)
    login_pass = models.CharField('ログインPass', max_length=255, null=True, blank=True)


# 章マスタ
class Shou(models.Model):
    class Meta:
        db_table = 'shou'

    shou_name = models.CharField('章名', max_length=255, null=True, blank=True)

# 問題マスタ
class Prob(models.Model):
    class Meta:
        db_table = 'prob'

    shou = models.ForeignKey(Shou, verbose_name='章番号',  on_delete=models.CASCADE)
    prob_num = models.IntegerField(verbose_name='問題番号', null=True, blank=True)
    title = models.CharField('問題タイトル', max_length=255, null=True, blank=True)
    prob_bun = models.CharField('問題文', max_length=5000, null=True, blank=True)
    sentaku_1 = models.CharField('選択肢１', max_length=255, null=True, blank=True)
    sentaku_2 = models.CharField('選択肢２', max_length=255, null=True, blank=True)
    sentaku_3 = models.CharField('選択肢３', max_length=255, null=True, blank=True)
    sentaku_4 = models.CharField('選択肢４', max_length=255, null=True, blank=True)
    seikai = models.IntegerField('正解番号', null=True, blank=True)
    kaisetsu = models.CharField('解説', max_length=5000, null=True, blank=True)

# 学習進捗
class Shintyoku(models.Model):
    class Meta:
        db_table = 'shintyoku'

    kaiin = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    shou = models.ForeignKey(Shou, on_delete=models.CASCADE)
    prob = models.ForeignKey(Prob, on_delete=models.CASCADE)
    seigo = models.CharField('正誤', max_length=255)
    answer_date = models.DateField('最終回答日', null=True, blank=True)
