# Generated by Django 2.2.1 on 2019-05-23 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carpool', '0006_auto_20190523_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='regularity',
            field=models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], default='1', max_length=1),
        ),
    ]
