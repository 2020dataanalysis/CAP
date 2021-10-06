# Generated by Django 3.1.7 on 2021-04-03 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PO',
            fields=[
                ('po_id', models.IntegerField(primary_key=True, serialize=False)),
                ('up_id', models.CharField(default='', max_length=15)),
                ('date', models.CharField(max_length=10)),
                ('ro', models.IntegerField()),
                ('invoice', models.CharField(max_length=20)),
                ('category', models.CharField(max_length=10)),
                ('vendor', models.CharField(max_length=30)),
                ('qty', models.CharField(max_length=1)),
                ('price', models.FloatField()),
                ('cost', models.FloatField()),
                ('transferred', models.CharField(max_length=1)),
                ('payables', models.CharField(max_length=1)),
                ('credit', models.CharField(max_length=1)),
                ('voided', models.CharField(max_length=1)),
                ('closed', models.CharField(max_length=1)),
            ],
        ),
    ]
