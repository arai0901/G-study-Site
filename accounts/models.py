from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    class Meta(AbstractUser.Meta):
        db_table = 'custom_user'

    corp = models.CharField('企業名', max_length=255, blank=True, null=True)
    corp_id = models.IntegerField('企業ID', blank=True, null=True)
    auth_edit = models.IntegerField('編集権限', blank=True, null=True)
    auth_view = models.IntegerField('確認権限', blank=True, null=True)
