# Generated by Django 3.2.5 on 2021-09-25 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cc', '0003_alter_ccm_posted_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ccm',
            name='date',
        ),
    ]
