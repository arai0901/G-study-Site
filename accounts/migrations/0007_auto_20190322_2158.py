# Generated by Django 2.1.5 on 2019-03-22 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20190322_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='auth_edit',
            field=models.IntegerField(blank=True, null=True, verbose_name='編集権限'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='auth_view',
            field=models.IntegerField(blank=True, null=True, verbose_name='確認権限'),
        ),
    ]
