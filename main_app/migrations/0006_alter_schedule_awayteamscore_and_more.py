# Generated by Django 4.2.7 on 2023-11-09 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_schedule_awayteamscore_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='awayteamscore',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='hometeamscore',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
