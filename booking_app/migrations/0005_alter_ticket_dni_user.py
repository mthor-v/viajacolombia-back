# Generated by Django 3.2.7 on 2021-10-21 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_app', '0004_route_id_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='dni_User',
            field=models.IntegerField(verbose_name='User'),
        ),
    ]