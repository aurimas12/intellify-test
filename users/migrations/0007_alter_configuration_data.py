# Generated by Django 3.2.20 on 2023-07-13 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_timeseries_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='data',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
