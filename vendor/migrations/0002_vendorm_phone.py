# Generated by Django 3.2.5 on 2021-09-20 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorm',
            name='phone',
            field=models.CharField(default='', max_length=14),
        ),
    ]
