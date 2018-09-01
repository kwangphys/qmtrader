# Generated by Django 2.0.6 on 2018-09-01 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yahoo', '0004_auto_20180901_2052'),
    ]

    operations = [
        migrations.CreateModel(
            name='EarningsPostCalendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField()),
                ('updated_by', models.CharField(default='matlidia', max_length=64)),
                ('ticker', models.CharField(max_length=16)),
                ('full_name', models.CharField(max_length=255)),
                ('fiscal_quarter_ending', models.CharField(max_length=16)),
                ('earnings_date', models.DateField()),
                ('time', models.CharField(blank=True, max_length=32)),
                ('consensus_eps_forecast', models.FloatField(null=True)),
                ('n_estimates', models.IntegerField(null=True)),
                ('eps', models.FloatField(null=True)),
                ('surprise', models.FloatField(null=True)),
                ('source', models.CharField(max_length=16)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]