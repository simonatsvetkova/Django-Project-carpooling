# Generated by Django 2.2.1 on 2019-05-23 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carpool', '0007_auto_20190523_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='regularity',
            field=models.CharField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], default='1', max_length=1),
        ),
    ]
