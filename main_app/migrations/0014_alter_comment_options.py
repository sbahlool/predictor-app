# Generated by Django 4.2.7 on 2023-11-12 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0013_alter_comment_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-date']},
        ),
    ]
