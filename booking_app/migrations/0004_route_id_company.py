# Generated by Django 3.2.7 on 2021-10-21 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_app', '0003_alter_user_dniuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='id_company',
            field=models.BigIntegerField(default=1, verbose_name='idCompany'),
        ),
    ]