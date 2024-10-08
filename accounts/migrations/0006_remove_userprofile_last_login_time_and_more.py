# Generated by Django 5.1.1 on 2024-09-15 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_userprofile_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='last_login_time',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='login_count',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='daily_login_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_login_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='monthly_login_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='weekly_login_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='yearly_login_count',
            field=models.IntegerField(default=0),
        ),
    ]
