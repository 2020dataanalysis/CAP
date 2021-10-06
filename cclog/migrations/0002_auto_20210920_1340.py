# Generated by Django 3.2.5 on 2021-09-20 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0005_auto_20210919_2255'),
        ('cclog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='vendor_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendor.vendormodel'),
        ),
        migrations.AddField(
            model_name='log',
            name='vendor_id_link',
            field=models.IntegerField(default=0),
        ),
    ]