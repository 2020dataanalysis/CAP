# Generated by Django 3.2.5 on 2021-09-18 00:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ccm',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
