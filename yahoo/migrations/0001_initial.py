# Generated by Django 2.0.6 on 2018-06-17 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EarningsCalendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='matlidia', max_length=64)),
                ('ticker', models.CharField(max_length=16)),
                ('full_name', models.CharField(max_length=255)),
                ('fiscal_quarter_ending', models.CharField(max_length=16)),
                ('earnings_date', models.DateField()),
                ('time', models.CharField(max_length=32)),
                ('consensus_eps_forecast', models.FloatField(null=True)),
                ('n_estimates', models.IntegerField()),
                ('is_confirmed', models.BooleanField()),
                ('source', models.CharField(max_length=16)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
