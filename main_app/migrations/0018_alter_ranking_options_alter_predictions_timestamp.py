# Generated by Django 4.2.7 on 2023-11-13 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0017_ranking'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ranking',
            options={'ordering': ['-totalpoints']},
        ),
        migrations.AlterField(
            model_name='predictions',
            name='timestamp',
            field=models.TimeField(default='15:00:00'),
        ),
    ]