# Generated by Django 3.2.5 on 2021-09-20 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0003_rename_vendorm_vendormodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendormodel',
            name='alias',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
