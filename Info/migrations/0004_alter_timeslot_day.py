# Generated by Django 5.1.8 on 2025-04-18 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Info', '0003_alter_schedule_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='day',
            field=models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')]),
        ),
    ]
