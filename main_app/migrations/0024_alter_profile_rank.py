# Generated by Django 4.2.7 on 2023-11-14 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0023_alter_comment_options_alter_profile_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='rank',
            field=models.IntegerField(default=0),
        ),
    ]
