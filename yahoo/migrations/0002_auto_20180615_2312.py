# Generated by Django 2.0.6 on 2018-06-15 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yahoo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nasdaqearningscalendar',
            name='consensus_eps_forecast',
            field=models.FloatField(null=True),
        ),
    ]
